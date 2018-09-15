from models import *
from anytree import AnyNode, RenderTree, LevelOrderGroupIter
from datetime import datetime, timedelta

# Assumption
# Workers   Morning Shift -- 8:00a - 2:00p      Evening Shift -- 2:00p - 10:00p
# Work Order has been assigned to workers on the basis of priority with minimum time of completion for all work orders till then
#

# get all the work orders except the "completed" ones


def get_all_orders():
    orders = Order.query.filter(Order.status != "completed").all()
    return orders

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


# get the oldest datetime comparing the current old time and datetime if that worker is assigned that work order
def get_total_time(TTC, worker_id, current_value):
    worker = Worker.query.get(worker_id)
    # get the ending shift datetime
    shift_time = worker.time_until_free.date()
    if worker.shift == 'morning':
        shift_time = datetime.time(14, 0, 0)
    else:
        shift_time = datetime.time(22, 0, 0)
    # add the time together to get the working time of worker during his/her shift hours
    worker.testing_time = add_time(
        worker.testing_time, timedelta(hours=TTC), shift_time)
    # return the oldest datetime
    if worker.testing_time > current_value:
        return worker.testing_time
    return current_value


# recover the best solution given the best leaf of a tree
def recover_best_path(best_node):
    res = []
    # go back to the root parent tracing from the best leaf and store work_id and worker_id in the list
    while best_node.depth != 0:
        res.append([best_node.work_id, best_node.worker_id])
        best_node = best_node.parent
    return res


# brute force all the scenarios with the help of tree. The path of the best value of the leaf through the tree gives the best scenario
def get_best_scenario(orders):
    # scenario starts with current datetime
    scenario = AnyNode(value=datetime.now())
    depth = 0

    for order in orders:
        partrees = []
        # get all the leaves in the last level
        for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
            partrees = nodes

            # iterate through all the leaves and grow more based on work assigned
            for partree in partrees:
                children = []

                # if "in_progress", get the latest time comparing the current latest time and time required by worker to complete
                if order.status == "in_progress":
                    worker = Worker.query.get(order.worker_id)
                    a = AnyNode(work_id=order.work_id, worker_id=order.worker_id, value=min(
                        worker.time_until_free, partree.value))
                    children.append(a)

                # else, brute force with all workers and get the latest time of completion
                else:
                    workers = get_all_workers(order.equipment_id)
                    for worker in workers:
                        a = AnyNode(work_id=order.work_id, worker_id=worker.worker_id, value=get_total_time(
                            order.time_to_completion, worker.worker_id, partree.value))
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
