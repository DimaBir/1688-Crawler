from flask import jsonify, request
import traceback

from . import web
from app.spiders.go2product import Go2Product


@web.route('/go2/product', methods=['GET'])
def crawl_go2_product():
    try:
        product = Go2Product()
        product = product.go(request.args.get('url'))
        return jsonify(product)
    except Exception as e:
        traceback.print_exc()
        resp = jsonify({'errcode': 500, 'errmsg': '抓取产品异常: ' + str(e)})
        resp.status_code = 500
        return resp
