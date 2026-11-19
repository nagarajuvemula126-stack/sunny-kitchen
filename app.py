
from flask import Flask, render_template_string, redirect, url_for, session, request
app = Flask(__name__)
app.secret_key = "sunny_store_secret"

products = [
    {"id": 1, "name": "Pressure Cooker", "price": 1499, "emoji": "🍲"},
    {"id": 2, "name": "Non-Stick Pan", "price": 699, "emoji": "🍳"},
    {"id": 3, "name": "Mixer Grinder", "price": 2499, "emoji": "🥤"},
    {"id": 4, "name": "Steel Containers", "price": 599, "emoji": "🥫"},
    {"id": 5, "name": "Vegetable Chopper", "price": 399, "emoji": "🥕"},
    {"id": 6, "name": "Knife Set", "price": 499, "emoji": "🔪"}
]

@app.route("/")
def home():
    cart = session.get("cart", {})
    count = sum(cart.values())

    return render_template_string("""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SUNNY KITCHEN STORE</title>
    <style>
    body {
        margin: 0;
        font-family: Arial;
        background: #f2f4f8;
    }
    header {
        background: #142850;
        color: white;
        text-align: center;
        padding: 20px;
    }
    .cart {
        color: white;
        text-decoration: none;
        background: #e67e22;
        padding: 12px;
        border-radius: 8px;
    }
    .products {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        padding: 15px;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .emoji { font-size: 48px; }
    button {
        background: #142850;
        color: white;
        border: 0;
        padding: 12px;
        border-radius: 8px;
    }
    </style>
    </head>
    <body>
    <header>
        <h1>🍳 SUNNY KITCHEN</h1>
        <p>Welcome Boss!</p>
        <a class="cart" href="/cart">🛒 Cart ({{count}})</a>
    </header>

    <h2 style="text-align:center">Kitchen Products</h2>

    <div class="products">
    {% for p in products %}
      <div class="card">
        <div class="emoji">{{p.emoji}}</div>
        <h3>{{p.name}}</h3>
        <h3>₹{{p.price}}</h3>
        <a href="/add/{{p.id}}">
          <button>Add to Cart</button>
        </a>
      </div>
    {% endfor %}
    </div>
    </body>
    </html>
    """, products=products, count=count)


@app.route("/add/<int:pid>")
def add(pid):
    if not any(p["id"] == pid for p in products):
        return "Product not found", 404

    cart = session.get("cart", {})
    key = str(pid)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return redirect(url_for("home"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for p in products:
        qty = cart.get(str(p["id"]), 0)
        if qty > 0:
            subtotal = p["price"] * qty
            total += subtotal
            items.append({
                "name": p["name"],
                "price": p["price"],
                "qty": qty,
                "subtotal": subtotal,
                "id": p["id"]
            })

    return render_template_string("""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Cart</title>
    </head>
    <body style="font-family:Arial;background:#f2f4f8;padding:20px">
    <h1>🛒 My Shopping Cart</h1>

    {% for item in items %}
      <div style="background:white;padding:15px;margin:10px;border-radius:10px">
        <h3>{{item.name}}</h3>
        Price: ₹{{item.price}}<br>
        Quantity: {{item.qty}}<br>
        Total: ₹{{item.subtotal}}
        <p><a href="/remove/{{item.id}}">Remove</a></p>
      </div>
    {% endfor %}

    <h2>Grand Total: ₹{{total}}</h2>
    {% if not items %}
      <p>Your cart is empty!</p>
    {% endif %}

    <a href="/">Continue Shopping</a>
    </body>
    </html>
    """, items=items, total=total)


@app.route("/remove/<int:pid>")
def remove(pid):
    cart = session.get("cart", {})

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("home"))

    items = []
    total = 0

    for p in products:
        qty = cart.get(str(p["id"]), 0)
        if qty:
            subtotal = p["price"] * qty
            total += subtotal
            items.append((p, qty, subtotal))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not phone or not address:
            return "Please fill all details!"

        order = {
            "name": name,
            "phone": phone,
            "address": address,
            "total": total,
            "items": items
        }

        orders = session.get("orders", [])
        orders.append(order)
        session["orders"] = orders
        session["cart"] = {}

        return render_template_string("""
        <h1>Order Successful!</h1>
        <h2>Thank you {{name}}!</h2>
        <h3>Order Total: ₹{{total}}</h3>
        <a href="/">Continue Shopping</a>
        """, name=name, total=total)

    return render_template_string("""
    <h1>🛒 SUNNY KITCHEN CHECKOUT</h1>
    <h2>Grand Total: ₹{{total}}</h2>
    <form method="POST">
        <input name="name" placeholder="Customer Name" required><br><br>
        <input name="phone" placeholder="Mobile Number"
        type="tel" required><br><br>
        <textarea name="address"
        placeholder="Delivery Address" required></textarea><br><br>
        <button type="submit">Place Order</button>
    </form>
    """, total=total)


    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("view_cart"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

























































