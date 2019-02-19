# -*- coding: utf-8 -*-

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def cron_clean_users(self):
        self.search([("login", "like", "tmp_%"), ("active", "=", False)]).filtered(
            lambda r: not r.login_date
        ).unlink()
        self.search([("login", "like", "tmp_%")]).filtered(lambda r: not r.login_date).write(
            {"active": False}
        )
