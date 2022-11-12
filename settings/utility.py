# конвертирует список с р[(3,), (5,)] к [3,5,...]
def _convert(list_convert):
    return [itm[0] for itm in list_convert]

def get_total_coast(BD,user_id):
    """
    Подсчет общей суммы заказа
    """
    # Получаю список всех товаров
    all_product_id = BD.select_all_product_id(user_id)
    # Получаю список стоимость по всем позициям заказа в виде обычного списка
    all_price = [BD.select_single_product_price(itm) for itm in all_product_id]
    # Получаю список количества по всем позициям заказа в виде обычного списка
    all_quantity = [BD.select_order_quantity(itm, user_id) for itm in all_product_id]
    # возврат общей стоимости товара
    return total_coast(all_quantity, all_price)

def get_total_quantity(BD, user_id):
    """
    Подсчет общего количества товаров
    """
    # Получаю список всех товаров
    all_product_id = BD.select_all_product_id(user_id)
    # Получаю список количества по всем позициям заказа в виде обычного списка
    all_quantity = [BD.select_order_quantity(itm, user_id) for itm in all_product_id]
    # возврат общего количества товаров
    return total_quantity(all_quantity)

def total_coast(list_quantity, list_price):
    order_total_coast = 0

    for ind, itm in enumerate(list_price):
        order_total_coast += list_price[ind] * list_quantity[ind]

    return order_total_coast

def total_quantity(list_quantity):
    order_total_quantity = 0

    for itm in list_quantity:
        order_total_quantity += itm

    return order_total_quantity