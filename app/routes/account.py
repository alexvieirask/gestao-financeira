''' Importação das configurações e serviços '''
from services.config import *
from services.forms_utils import *

@app.route("/form/new_account", methods = ["POST"])
@jwt_required()
def form_new_account():
    try:
        useremail = get_jwt_identity()
        user = DB_User.get_record_by_email(useremail) 
        fields = request.get_json()

        if not fields_empty(fields):
            account_exists = DB_Account.get_record_by_name(fields["account_name"], user["id"])

            if not account_exists:
                opening_balance = int(fields["opening_balance"]) 

                DB_Account.insert_record(
                    fields["account_name"],
                    opening_balance,
                    opening_balance,
                    user["id"]
                )
                
                response = jsonify({"status":200, "details":"Conta registrada."})
            else:
                response = jsonify({"status":250, "details":"Você já possui uma conta com esse nome."})    
        else:
            response = jsonify({"status":250, "details":"Faltou preencher campos obrigatórios."})

    except Exception as error:
        response = jsonify({"status":777, "details":str(error)})
    
    return response

@app.route("/account/max_amount")
@jwt_required() 
def account_max_amount(): 
    try:
        useremail = get_jwt_identity()
        user = DB_User.get_record_by_email(useremail) 
        account_with_max_amount = DB_Account.get_account_with_max_amount(user["id"])

        response = jsonify({"status":200, "details": account_with_max_amount })

    except Exception as error:
        response = jsonify({"status":777, "details":str(error)})
    
    return response