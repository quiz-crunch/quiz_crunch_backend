import logging
import traceback

from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.repository.unit_of_work import UnitOfWork
from manage.model.user_model import UserModel
from manage.service.user_service import UserService

bp = Blueprint('user', __name__)
logger = logging.getLogger('user')


@bp.route('/list', methods=['GET'])
@inject
def route_get_dog_list(
        user_service: UserService = Provide[
            Container.example_module_container.user_service
        ],
):
    result = ApiResponse()

    try:
        dog_list = user_service.get_list()
        result.data = dog_list

    except Exception as e:
        traceback.print_exc()
        logger.error(str(e))
        result = ApiResponse(code=500, message=str(e))

    return jsonify(result.to_json())


@bp.route('/detail/<string:user_id>', methods=['GET'])
@inject
def route_get_detail(
        user_id: str,
        user_service: UserService = Provide[
            Container.example_module_container.user_service
        ],
):
    result = ApiResponse()

    try:
        detail = user_service.get_detail(
            user_id=user_id
        )
        detail.convert_names = False
        result.data = detail.model_dump()

    except Exception as e:
        traceback.print_exc()
        logger.error(str(e))
        result = ApiResponse(code=500, message=str(e))

    return jsonify(result.to_json())


@bp.route('/upload', methods=['POST'])
@inject
def route_upload(
        user_service: UserService = Provide[
            Container.example_module_container.user_service
        ],
):
    result = ApiResponse()

    try:
        file = request.files['file']
        specify_name = request.form.get('specifyName', None)
        file_name = file.filename
        if specify_name:
            file_name = specify_name
        user_service.upload(
            file=file,
            file_name=file_name,
        )

    except Exception as e:
        traceback.print_exc()
        logger.error(str(e))
        result = ApiResponse(code=500, message=str(e))

    return jsonify(result.to_json())


@bp.route('/add', methods=['POST'])
@inject
def route_add(
        uow: UnitOfWork = Provide[Container.example_module_container.unit_of_work],
        user_service: UserService = Provide[
            Container.example_module_container.user_service
        ],
):
    result = ApiResponse()

    try:
        params = request.get_json(silent=True)

        with uow:
            result.data = user_service.add(
                user=UserModel(**params)
            )
            uow.commit()

    except Exception as e:
        traceback.print_exc()
        logger.error(str(e))
        result = ApiResponse(code=500, message=str(e))

    return jsonify(result.to_json())
