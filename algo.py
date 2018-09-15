from models import *
from anytree import AnyNode, RenderTree, LevelOrderGroupIter
from datetime import datetime, timedelta

# Assumption
# Workers   Morning Shift -- 8:00a - 2:00p      Evening Shift -- 2:00p - 10:00p
# Work Order has been assigned to workers on the basis of priority with minimum time of completion for all work orders till then
#


def get_all_orders():
    orders = Order.query.filter(Order.status != "completed").all()
    return orders


def get_all_workers(equipment_id):
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers
    certification = Certification.query.filter_by(
        equipment_type=equipment.equipment_type)
    workers = certification.worker_id

    return workers


def add_time(a, b, shift_time):
    if (a + b) <= shift_time:
        return a+b
    else:
        shift_time = shift_time + timedelta(hours=24)
        b = b + timedelta(hours=16)
        return add_time(a, b, shift_time)


def get_total_time(TTC, worker_id, current_value):
    worker = Worker.query.get(worker_id)
    shift_time = worker.time_until_free.date()
    if worker.shift == 'morning':
        shift_time = datetime.time(14, 0, 0)
    else:
        shift_time = datetime.time(22, 0, 0)
    worker.testing_time = add_time(
        worker.testing_time, timedelta(hours=TTC), shift_time)
    if worker.testing_time > current_value:
        return worker.testing_time
    return current_value


def recover_best_path(best_node):
    res = []
    while best_node.depth != 0:
        res.append(best_node.work_id, best_node.worker_id)
        best_node = best_node.parent
    return res


def get_best_scenario(orders):
    scenario = AnyNode(value=datetime.now())
    depth = 0

    for order in orders:
        partrees = []

        for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
            partrees = nodes

            for partree in partrees:
                children = []
                if order.status == "in_progress":
                    a = AnyNode(work_id=order.work_id, worker_id=order.worker_id, value=get_total_time(
                        order.time_to_completion, order.worker_id, partree.value))
                    children.append(a)

                else:
                    workers = get_all_workers(order.equipment_id)
                    for worker in workers:
                        a = AnyNode(work_id=order.work_id, worker_id=worker.worker_id, value=get_total_time(
                            order.time_to_completion, worker.worker_id, partree.value))
                        children.append(a)

                partree.children = children

        depth = depth + 1

    for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
        partrees = nodes
    # get the node that has minimum value in partress
    best = partrees.index(min(partrees.value))
    # pick the best path as array and return it
    reversed_result = recover_best_path(best)
    result = reversed_result.reverse()
    return result
