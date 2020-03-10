from app import logger


def log_request(method, request_url, center_id, entity_type, entity_id):
    """
    Function that add information to log file.
    :param method: request method.
    :param request_url: request url.
    :param center_id: id of user that send request.
    :param entity_type: type of entity that user add or change.
    :param entity_id: id of entity that we add/delete/modify.
    :return:
    """
    logger.info('method %s - request_url %s - center_id %s - entity_type %s - entity_id %s',
                method, request_url, center_id, entity_type, entity_id)
