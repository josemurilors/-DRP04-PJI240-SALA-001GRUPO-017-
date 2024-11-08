from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS  # Importa a função CORS para lidar com requisições de diferentes origens

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Adiciona suporte a CORS na aplicação, permitindo requisições de diferentes origens
CORS(app)

# Define a URI de conexão com o banco de dados MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/estoque"

# Estabelece conexão com o MongoDB usando a URI definida
client = MongoClient(app.config["MONGO_URI"])

# Acessa o banco de dados estoque no cliente MongoDB
mongo = client.estoque

# Define a rota para a página inicial da aplicação
@app.route("/")
def index():
    
    return render_template("stock-manager.html")

# Define a rota para obter todos os produtos
@app.route("/products", methods=["GET"])
def get_all_products():
    # Busca todos os produtos na coleção products do banco de dados
    products = mongo.products.find()
    
    # Retorna os produtos em formato JSON com campos id, name, quantity e description
    return jsonify([{"id": str(product["_id"]), "name": product["name"], "quantity": product["quantity"], "description": product["description"]} for product in products])

# Define a rota para adicionar um novo produto
@app.route("/products", methods=["POST"])
def add_product():
    # Obtém os dados do produto da requisição em formato JSON
    data = request.get_json()
    
    # Cria um dicionário com os dados do produto
    product = {"name": data["name"], "quantity": data["quantity"], "description": data["description"]}
    
    # Insere o novo produto na coleção products
    mongo.products.insert_one(product)
    
    # Retorna uma mensagem de sucesso em formato JSON
    return jsonify({"message": "Product added successfully"})

# Define a rota para obter um produto específico por ID
@app.route("/products/<id>", methods=["GET"])
def get_product(id):
    # Busca o produto com o ID fornecido na coleção products
    product = mongo.products.find_one({"_id": ObjectId(id)})
    
    if product:
        # Retorna os detalhes do produto em formato JSON
        return jsonify({"id": str(product["_id"]), "name": product["name"], "quantity": product["quantity"], "description": product["description"]})
    else:
        # Retorna uma mensagem de erro e código de status 404 se o produto não for encontrado
        return jsonify({"message": "Product not found"}), 404

# Define a rota para atualizar um produto específico por ID
@app.route("/products/<id>", methods=["PUT"])
def update_product(id):
  
    data = request.get_json()
    
    # Atualiza a quantidade do produto com o ID fornecido na coleção products
    mongo.products.update_one({"_id": ObjectId(id)}, {"$set": {"quantity": data["quantity"]}})
    
   
    return jsonify({"message": "Product updated successfully"})

# Define a rota para deletar um produto específico por ID
@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    # Remove o produto com o ID fornecido da coleção products
    mongo.products.delete_one({"_id": ObjectId(id)})
    
   
    return jsonify({"message": "Product deleted successfully"})

# Inicia a aplicação Flask se este script for executado diretamente
if __name__ == "__main__":
    # Executa a aplicação Flask com o modo de depuração ativado
    app.run(debug=True)