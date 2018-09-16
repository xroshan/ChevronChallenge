from models import *
from anytree import AnyNode, RenderTree, LevelOrderGroupIter
from datetime import datetime, timedelta
from sqlalchemy import or_

# Assumption
# Workers   Morning Shift -- 8:00a - 2:00p      Evening Shift -- 2:00p - 10:00p
# Work Order has been assigned to workers on the basis of priority with minimum time of completion for all work orders till then
# Priority.. 1 -- highest priority and 5 -- lowest priority

# get all the work orders except the "completed" ones
def get_all_orders():
    orders = Order.query.filter(Order.status != "completed").order_by(Order.priority).all()
    return orders 

# get all the work orders "completed" or "in_progress" ones
def get_all_pending_orders():
    orders = Order.query.filter(
        or_(Order.status == "pending", Order.status == "assigned")).order_by(Order.priority).all()
    return orders 


# get all the work orders "in_progress" ones or "assigned" ones
def get_all_assigned_orders():
    orders = Order.query.filter(
        or_(Order.status == "in_progress",  Order.status == "assigned")).order_by(Order.priority).all()
    return orders 


# get all the workers who can fix the "equipment_id"
def get_all_workers(equipment_id):
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers having that certification
    certifications = Certification.query.filter_by(
        equipment_type=equipment.equipment_type).all()

    workers = []
    for cert in certifications:
        workers.append(cert.worker)

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
# def get_total_time(TTC, id, res):
#     worker = Worker.query.get(id)
#     shift_start_time
#     shift_end_time
#     shift_time = datetime.now()
#     # get the ending shift datetime
#     if worker.time_until_free > datetime.now():
#         shift_time = shift_time.replace(year = worker.time_until_free.year(), month= worker.time_until_free.month(), day= worker.time_until_free.day())
#     if worker.shift == 'morning':
#         shift_time = shift_time.replace(hour=14, minute=0, second=0)
#     else:
#         shift_time = shift_time.replace(hour=22, minute=0, second=0)
#     # add the time together to get the working time of worker during his/her shift hours
#     if worker.time_until_free < datetime.now():
#         testing_time = add_time(datetime.now(), timedelta(hours = TTC), shift_time)
#     else:
#         testing_time = add_time(
#             res[worker.id], timedelta(hours=TTC), shift_time)
#     # return the test_time till now
#     return testing_time

def get_total_time(TTC, id, res):
    worker = Worker.query.get(id)
    end_time = res[worker.id] + timedelta(hours = TTC)
    return end_time


# recover the best solution given the best leaf of a tree
def recover_best_path(best_node):
    res = dict()
    # go back to the root parent tracing from the best leaf and store work_id as key and return id, start_time and end_time in it
    while best_node.depth != 0:
        res[best_node.work_id] = [best_node.id,
                                        best_node.st_time, best_node.end_time];
        best_node = best_node.parent
    return res


# brute force all the scenarios with the help of tree. The path of the best value of the leaf through the tree gives the best scenario
def get_best_scenario(orders):
    # scenario starts with current datetime
    scenario = AnyNode(testing_infos=dict(), value=datetime.now())
    depth = 0
    for order in orders:
        partrees = []
        # get all the leaves in the last level
        for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
            partrees = nodes

        # iterate through all the leaves and grow more based on work assigned
        for partree in partrees:
            children = []
            res = dict()
            # store all worker_time completion testing as key and value
            if not partree.is_root:
                res = partree.parent.testing_infos

            # if "in_progress", get the latest time comparing the current latest time and time required by worker to complete
            if order.status == "in_progress":
                worker = Worker.query.get(order.worker_id)
                # set worker testing time to time until free as it has already been assigned "in_progress"
                res[worker.id] = worker.time_until_free
                # node stores all the required variables such as previous work_info, start_time, end_time, worker info and values
                a = AnyNode(testing_infos=res, work_id=order.id, st_time=order.est_start_time, end_time=order.est_end_time, id=order.id, value=max(order.est_end_time
                    , partree.value))
                children.append(a)

            # else, brute force with all workers and get the latest time of completion
            else:
                workers = get_all_workers(order.equipment_id)
                for worker in workers:
                    # if worker has not been assigned earlier work, set his/her leisure time
                    if not worker.id in res:
                        res[worker.id] = worker.time_until_free
                    # have value for the start_time of work as well as the end time of work
                    start_time = res[worker.id]
                    res[worker.id] = get_total_time(
                        order.time_to_completion, worker.id, res)
                    a = AnyNode(testing_infos=res, work_id=order.id, id=worker.id, st_time=start_time,
                                end_time=res[worker.id], value=max(res[worker.id], partree.value))
                    children.append(a)

            # add the leaves to the current parent node
            partree.children = children
        # go deep 1 more level each time one work order is processed
        depth = depth + 1
    # get the leaves of the tree
    for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
        partrees = nodes
    # get the node that has minimum value in partress
    best = partrees[0]
    min_val = partrees[0].value
    for p in partrees:
        if p.value < min_val:
            min_val = p.value
            best = p
    # pick the best path as array and return it
    result = recover_best_path(best)
    return result


# assign the task once we get the best scenario
def assign_task():
    orders = get_all_pending_orders()
    best = get_best_scenario(orders)
    # for each order, assign worker, estimated start time and estimated end time
    for order in orders:
        order.worker_id = best[order.id][0]
        order.est_start_time = best[order.id][1]
        order.est_end_time = best[order.id][2]
        order.status = 'assigned'
        
    # update database
    db.session.commit()


# check everytime if the task has been completed or is going to start
def check_time():
    orders = get_all_assigned_orders()
    for order in orders:
        print(order.est_start_time)
        # if estimated end time is greater than current time, then the work is completed
        if order.est_end_time < datetime.now():
            order.status = 'completed'

        # if estimated start time is greater than current time, then start the work i.e. "in_progress".. worker time_until_free is updated
        if order.est_start_time < datetime.now():
            order.status = 'in_progress'
            worker = Worker.query.get(order.id)
            worker.time_until_free = order.est_end_time
    # update database
    db.session.commit()


def update_worker_time():
    workers = Worker.query.all()
    for worker in workers:
        if worker.time_until_free is None:
            worker.time_until_free = datetime.now()
        elif worker.time_until_free < datetime.now():
            worker.time_until_free = datetime.now()
        db.session.commit()


# this function gets called when clients adds their work order request
def main():
    update_worker_time()
    check_time()
    assign_task()
    check_time()
