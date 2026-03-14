import streamlit as st
from sqlalchemy import text
from db import engine

st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.title("📦 Inventory Management")

# ---------- Fetch products ----------
@st.cache_data(ttl=10)
def fetch_products():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                product_id,
                name,
                category,
                price,
                stock_quantity
            FROM products
            ORDER BY product_id
        """))
        return result.fetchall(), result.keys()


rows, columns = fetch_products()

# Convert to editable table format
data = [dict(zip(columns, row)) for row in rows]

st.subheader("Edit Inventory")

edited_data = st.data_editor(
    data,
    use_container_width=True,
    num_rows="fixed",
    key="inventory_editor"
)

# ---------- Save changes ----------
if st.button("💾 Save Changes"):
    with engine.begin() as conn:
        for row in edited_data:
            conn.execute(
                text("""
                    UPDATE products
                    SET
                        price = :price,
                        stock_quantity = :stock_quantity
                    WHERE product_id = :product_id
                """),
                {
                    "price": row["price"],
                    "stock_quantity": row["stock_quantity"],
                    "product_id": row["product_id"]
                }
            )

    st.success("Inventory updated successfully ✅")
    st.cache_data.clear()
