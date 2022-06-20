from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_history():
        sql = "SELECT a.action_description , d.name, h.datetime, h.value, h.comment FROM carcontrol.History as h "
        sql += "inner join carcontrol.Actions as a on h.actions_id = a.actions_id "
        sql += "inner join carcontrol.Devices as d on h.device_id = d.device_id "
        sql += "order by datetime desc "
        sql += "limit 50;"
        return Database.get_rows(sql)

    @staticmethod
    def read_device_values_by_id(id):
        sql = "select value, datetime from carcontrol.History "
        sql += "where device_id = %s "
        sql += "order by datetime desc "
        sql += "limit 20"
        params = [id]
        return Database.get_rows(sql, params)



    # @staticmethod
    # def read_status_lamp_by_id(id):
    #     sql = "SELECT * from lampen WHERE id = %s"
    #     params = [id]
    #     return Database.get_one_row(sql, params)

    # @staticmethod
    # def update_status_lamp(id, status):
    #     sql = "UPDATE lampen SET status = %s WHERE id = %s"
    #     params = [status, id]
    #     return Database.execute_sql(sql, params)

    # @staticmethod
    # def update_status_alle_lampen(status):
    #     sql = "UPDATE lampen SET status = %s"
    #     params = [status]
    #     return Database.execute_sql(sql, params)


    @staticmethod
    def Add_measurement(device_id, data, time, comment):
        sql = "INSERT INTO History (actions_id, device_id, datetime, value, comment) VALUES (1, %s, %s, %s, %s)"
        params = [device_id, time, data, comment]
        return Database.execute_sql(sql, params)

    @staticmethod
    def Add_excecute(device_id,time, comment):
        sql = "INSERT INTO History (actions_id, device_id, datetime, comment) VALUES (2, %s, %s, %s)"
        params = [device_id, time, comment]
        return Database.execute_sql(sql, params)