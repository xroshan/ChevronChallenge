from models import *
from anytree import AnyNode, RenderTree, LevelOrderGroupIter


def get_all_orders():
    orders = Order.query.all()
    return orders


def get_all_workers(equipment_id):
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers
    certification = Certification.query.filter_by(
        equipment_type=equipment.equipment_type)
    workers = certification.worker_id

    return workers


def get_total_time(TTC, worker, current_value):
    worker.total_time += TTC
    if worker.total_time > current_value:
        return worker.total_time
    return current_value


def recover_best_path(best_node):
    res = []
    while best_node.depth != 0:
        res.append(best_node.work_id, best_node.worker_id)
        best_node = best_node.parent
    return res


def get_best_scenario(orders):
    scenario = AnyNode(value=0)
    depth = 0

    for order in orders:
        workers = get_all_workers(order.equipment_id)
        partrees = []

        for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
            partrees = nodes

            for partree in partrees:
                children = []

                for worker in workers:
                    a = AnyNode(work_id=order.work_id, worker_id=worker.worker_id, value=get_total_time(
                        order.time_to_completion, worker, partree.value))
                    children.append(a)
                    partree.children = children

        depth = depth + 1

    for nodes in LevelOrderGroupIter(scenario, maxlevel=depth + 1):
        partrees = nodes
    # get the node that has minimum value in partress
    best = partrees.index(min(partrees.value))

    reversed_result = recover_best_path(best)
    result = reversed_result.reverse()
    return result
    # pick the best path as array and return it
