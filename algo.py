from models import *
from anytree import Node, RenderTree, LevelOrderGroupIter


def get_pending_orders():
    orders = Order.query.filter_by(
        status="pending").order_by(Order.priority).all()
    return orders


def is_worker_free(worker_id):
    worker = Worker.query.get(worker_id)

    for order in worker.orders:
        if order.status == "in_progress":
            return False

    return True


def get_all_workers(equipment_id):
    # get equipment type id
    equipment = Equipment.query.get(equipment_id)

    # get workers
    certification = Certification.query.filter_by(
        equipment_type=equipment.equipment_type)
    workers = certification.worker_id
    
    return workers

def sort_workers(workers):
    #sort workers according to their nearest time of completion


def assign_worker(workers, order_id):
    #check if workers are in_progress or assigned
    #check if workers can finish in his shift
    order = Order.query.get(order_id)
    order.worker_id = worker_id
    order.status = "in_progress"
    db.commit()


def later_assign_worker(worker_id, order_id):
    #need nearest time of completion



# function worker_id[] whoIsFree(Equipment type) -- Gives me all free workers who has equipment skills

# function worker_id leastSkill(worker_id[], equipment type) -- Gives me worker id with least skill among all

# function assignWork(worker_id, workOrder_id) -- assign work to worker

# function work_id[] get_work() -- get all the work request order in queue


def on_work_order_request():
    orders = get_pending_orders()
    for order in orders
        workers = get_all_workers(order.equipment_id)
        workers = sort_workers(workers)
        assign_worker(workers,order.order_id)
        if(len(workers) == 0):
            # assign next free worker
        else:
            workers = get_all_workers(equipment_id)
            #workers sort them according to their time nearest time of completion
            assign_worker(workers[0].worker_id, order.order_id)


# arrange them in priority order()
# apply work algorithm(work_id)


# if whoIsFree != null:
#    Assign work to leastSkilled worker
# else
#   enque(work_order)


#####################
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
    

def get_best_scenario(orders):
    scenario = anyNode(value = 0);
    depth = 0

    for order in orders    
        workers = get_all_workers(order.equipment_id)
        partrees = []
        
        for nodes in LevelOrderGroupIter(scenario, maxLevel = depth + 1)
            partrees = nodes
            
            for partree in partrees
                children = []

                for worker in workers
                    a = AnyNode(work_id = order.work_id, worker_id = worker.worker_id, value = get_total_time(order, worker, partree))
                    children.append(a)
                    partree.children = children
        depth++

