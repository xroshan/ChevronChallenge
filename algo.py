from models import *


def get_pending_orders():
    orders = Order.query.filter_by(
        status="pending").order_by(Order.priority).all()
    return orders


def get_free_workers(equipment_id):
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers
    certification = Certification.query.filter_by(
        equipment_type=equipment.equipment_type)
    workers = certification.worker_id

    res = []

    for worker in workers:
        if is_worker_free(worker.id):
            res.append(worker)

    return res


def is_worker_free(worker_id):
    worker = Worker.query.get(worker_id)

    for order in worker.orders:
        if order.status == "in_progress":
            return False

    return True


def get_all_workers(equipment_id)
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers
    certification = Certification.query.filter_by(
        equipment_type=equipment.equipment_type)
    workers = certification.worker_id
    
    return workers


def assign_worker(worker_id, order_id):
    order = Order.query.get(order_id)
    order.worker_id = worker_id
    order.status = "in_progress"
    db.commit()


def later_assign_worker(worker_id, order_id)
    #need nearest time of completion



# function worker_id[] whoIsFree(Equipment type) -- Gives me all free workers who has equipment skills

# function worker_id leastSkill(worker_id[], equipment type) -- Gives me worker id with least skill among all

# function assignWork(worker_id, workOrder_id) -- assign work to worker

# function work_id[] get_work() -- get all the work request order in queue


def on_work_order_request():
    orders = get_pending_orders()
    for order in orders
    workers = get_free_workers(order.equipment_id)
    if(len(workers) == 0):
            # assign next free worker
        else:
            assign_worker(workers[0].worker_id, order.order_id)


# arrange them in priority order()
# apply work algorithm(work_id)


# if whoIsFree != null:
#    Assign work to leastSkilled worker
# else
#   enque(work_order)
