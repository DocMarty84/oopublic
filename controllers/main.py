# -*- coding: utf-8 -*-

import uuid

from odoo import http
from odoo.http import request
from odoo.service import security


class PublicController(http.Controller):
    @http.route("/public", type="http", auth="none", sitemap=False)
    def public(self):
        if not request.session.uid:
            tmp_login = "tmp_{}".format(uuid.uuid4().hex)
            tmp = (
                request.env["res.users"]
                .sudo()
                .create(
                    {
                        "name": "",
                        "login": tmp_login,
                        "password": tmp_login,
                        "lang": False,
                        "company_id": request.env.ref("base.main_company").id,
                        "company_ids": [(4, request.env.ref("base.main_company").id)],
                    }
                )
            )
            request.session.uid = tmp.id
            request.env["res.users"]._invalidate_session_cache()
            request.session.session_token = security.compute_session_token(
                request.session, request.env
            )
            return http.local_redirect("web", keep_hash=True)
        return http.local_redirect("/", query=request.params, keep_hash=True)
