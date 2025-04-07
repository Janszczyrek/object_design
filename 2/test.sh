#!/bin/bash

API_URL="http://localhost:35545/api/product"
CONTENT_TYPE="Content-Type: application/json"


echo -e "\nFetching initial product list..."
PRODUCTS=$(curl -s -X GET "$API_URL")
echo "Initial products: $PRODUCTS"

echo -e "\nClearing existing products..."
PRODUCT_IDS=$(echo $PRODUCTS | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
for ID in $PRODUCT_IDS; do
    echo "Deleting product with ID..."
    DELETE_RESPONSE=$(curl -s -X DELETE "$API_URL/$ID")
done

echo -e "\nVerifying products are cleared..."
PRODUCTS=$(curl -s -X GET "$API_URL")
if [ "$PRODUCTS" = "[]" ]; then
    echo -e "Product list is empty"
else
    echo -e "Product list is not empty"
fi

echo -e "\nCreating a new product with valid data..."
CREATE_RESPONSE=$(curl -s -X POST "$API_URL/new" \
    -H "$CONTENT_TYPE" \
    -d '{"name":"Banana","price":1.99,"description":"a Banana"}')
PRODUCT_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "Create response: $CREATE_RESPONSE"


echo -e "\nFetching the created product...}"
FETCH_RESPONSE=$(curl -s -X GET "$API_URL/$PRODUCT_ID")
echo -e "\nUpdating the product..."
UPDATE_RESPONSE=$(curl -s -X PUT "$API_URL/$PRODUCT_ID/edit" \
    -H "$CONTENT_TYPE" \
    -d '{"name":"Apple","price":0.99,"description":"an Apple"}')
echo "Update response: $UPDATE_RESPONSE"

echo -e "\nVerifying the product update..."
VERIFY_RESPONSE=$(curl -s -X GET "$API_URL/$PRODUCT_ID")
echo "Updated product: $VERIFY_RESPONSE"
if echo $VERIFY_RESPONSE | grep -q "Apple"; then
    echo -e "Product was successfully updated"
else
    echo -e "Product update verification failed"
fi

echo -e "\nDeleting the product..."
DELETE_RESPONSE=$(curl -s -X DELETE "$API_URL/$PRODUCT_ID")

echo -e "\nVerifying product deletion..."
VERIFY_DELETE=$(curl -s -X GET "$API_URL/$PRODUCT_ID")
if echo $VERIFY_DELETE | grep -q "Not Found"; then
    echo -e "Product was successfully deleted"
else
    echo -e "Product deletion verification failed"
fi

echo -e "\nFinal check of all products..."
FINAL_PRODUCTS=$(curl -s -X GET "$API_URL")
echo "Final product list: $FINAL_PRODUCTS"
