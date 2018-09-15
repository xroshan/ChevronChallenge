from models import *
from anytree import AnyNode, RenderTree, LevelOrderGroupIter
from datetime import datetime, timedelta

# Assumption
# Workers   Morning Shift -- 8:00a - 2:00p      Evening Shift -- 2:00p - 10:00p
# Work Order has been assigned to workers on the basis of priority with minimum time of completion for all work orders till then
# Priority.. 1 -- highest priority and 5 -- lowest priority

# get all the work orders except the "completed" ones
def get_all_orders():
    orders = Order.query.filter(Order.status != "completed").all()
    orders = priortize_orders(orders)
    return orders

# get all the work orders except the "completed ones" or "in_progress" ones
def get_all_assigned_orders():
    orders = Order.query.filter(
        Order.status != "completed" or Order.status != "in_progress").all()
    return orders


# sort the work orders based on their priority level
def priortize_orders(orders):
    return orders.sort(key=priortize_orders_helper)


# helper to priortize_order function
def priortize_orders_helper(ord):
    return ord.priority


# get all the workers who can fix the "equipment_id"
def get_all_workers(equipment_id):
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers having that certification
    certification = Certification.query.filter_by(
        equipment_type=equipment.equipment_type)
    workers = certification.worker_id

    return workers


# add two times together in such a way that the time is included during the shift hours the worker
def add_time(a, b, shift_time):
    if (a + b) <= shift_time:
        # if the sum of time is included during the shift hour return it
        return a+b
    else:
        # else include the time in next shift hours or else, include it in next shift hour
        shift_time = shift_time + timedelta(hours=24)
        b = b + timedelta(hours=16)
        return add_time(a, b, shift_time)


# get estimated start time and estimated end time for a work for that worker
def get_total_time(TTC, worker_id, res):
    worker = Worker.query.get(worker_id)
    # get the ending shift datetime
    shift_time = worker.time_until_free.date()
    if worker.shift == 'morning':
        shift_time = datetime.time(14, 0, 0)
    else:
        shift_time = datetime.time(22, 0, 0)
    # add the time together to get the working time of worker during his/her shift hours
    testing_time = add_time(
        res[worker.worker_id], timedelta(hours=TTC), shift_time)
    # return the test_time till now
    return testing_time


# recover the best solution given the best leaf of a tree
def recover_best_path(best_node):
    res = []
    # go back to the root parent tracing from the best leaf and store work_id as key and return worker_id, start_time and end_time in it
    while best_node.depth != 0:
        res.append([best_node.work_id, [best_node.worker_id,
                                        best_node.st_time, best_node.end_time]])
        best_node = best_node.parent
    return res


# brute force all the scenarios with the help of tree. The path of the best value of the leaf through the tree gives the best scenario
def get_best_scenario(orders):
    # scenario starts with current datetime
    scenario = AnyNode(testing_infos=[], value=datetime.now())
    depth = 0

    for order in orders:
        partrees = []
        # get all the leaves in the last level
        for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
            partrees = nodes

            # iterate through all the leaves and grow more based on work assigned
            for partree in partrees:
                children = []
                # store all worker_time completion testing as key and value
                res = partree.parent.testing_infos

                # if "in_progress", get the latest time comparing the current latest time and time required by worker to complete
                if order.status == "in_progress":
                    worker = Worker.query.get(order.worker_id)
                    # set worker testing time to time until free as it has already been assigned "in_progress"
                    res[worker.worker_id] = worker.time_until_free
                    # node stores all the required variables such as previous work_info, start_time, end_time, worker info and values
                    a = AnyNode(testing_infos=res, work_id=order.work_id, st_time=datetime.now(), end_time=res[worker.worker_id], worker_id=order.worker_id, value=min(
                        worker.time_until_free, partree.value))
                    children.append(a)

                # else, brute force with all workers and get the latest time of completion
                else:
                    workers = get_all_workers(order.equipment_id)
                    for worker in workers:
                        # if worker has not been assigned earlier work, set his/her leisure time
                        if not worker.worker_id in res:
                            res[worker.worker_id] = worker.time_until_free
                        # have value for the start_time of work as well as the end time of work
                        start_time = res[worker.worker_id]
                        res[worker.worker_id] = get_total_time(
                            order.time_to_completion, worker.worker_id, res)
                        a = AnyNode(testing_infos=res, work_id=order.work_id, worker_id=worker.worker_id, st_time=start_time,
                                    end_time=res[worker.worker_id], value=max(res[worker.worker_id], partree.value))
                        children.append(a)

                # add the leaves to the current parent node
                partree.children = children
        # go deep 1 more level each time one work order is processed
        depth = depth + 1

    # get the leaves of the tree
    for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
        partrees = nodes
    # get the node that has minimum value in partress
    best = partrees.index(min(partrees.value))
    # pick the best path as array and return it
    reversed_result = recover_best_path(best)

    # reverse the list in time wise
    result = reversed_result.reverse()
    return result


# assign the task once we get the best scenario
def assign_task():
    orders = get_all_assigned_orders()
    best = get_best_scenario(orders)
    # for each order, assign worker, estimated start time and estimated end time
    for order in orders:
        order.worker_id = best[order.work_id][0]
        order.est_start_time = best[order.work_id][1]
        order.est_end_time = best[order.work_id][2]
    # update database
    db.session.commit()


# check everytime if the task has been completed or is going to start
def check_time():
    orders = get_all_orders()
    for order in orders:
        # if estimated end time is greater than current time, then the work is completed
        if order.est_end_time > datetime.now():
            order.status = 'completed'

        # if estimated start time is greater than current time, then start the work i.e. "in_progress".. worker time_until_free is updated
        if order.est_start_time > datetime.now():
            order.status = 'in_progress'
            worker = Worker.query.get(order.worker_id)
            worker.time_until_free = order.est_end_time
    # update database
    db.session.commit()


# this function gets called when clients adds their work order request
def main():
    check_time()
    assign_task()
    check_time()
