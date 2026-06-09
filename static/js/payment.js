document.addEventListener('DOMContentLoaded', function () {
    const foodItemSelect = document.getElementById('foodItem');
    const quantityInput = document.getElementById('quantity');
    const addToOrderButton = document.getElementById('addToOrder');
    const orderList = document.getElementById('orderList');
    const totalCostSpan = document.getElementById('totalCost');
    const paymentForm = document.getElementById('paymentForm');
    const paymentUrl = paymentForm.getAttribute('data-url'); // Added this line

    let orderItems = [];

    function updateOrderSummary() {
        const items = orderList.querySelectorAll('li');
        let totalCost = 0;

        items.forEach(item => {
            const priceText = item.getAttribute('data-price');
            totalCost += parseFloat(priceText);
        });

        totalCostSpan.textContent = `₹${totalCost.toFixed(2)}`;  // Fixed template literal
    }

    function addToOrder() {
        const selectedOption = foodItemSelect.options[foodItemSelect.selectedIndex];
        const foodName = selectedOption.text;
        const foodPrice = parseFloat(selectedOption.getAttribute('data-price'));
        const quantity = parseInt(quantityInput.value);
        const totalPrice = foodPrice * quantity;

        if (foodName && quantity > 0) {
            const orderItem = document.createElement('li');
            orderItem.textContent = `${foodName} - Quantity: ${quantity} - Price: ₹${totalPrice.toFixed(2)}`;  // Fixed template literal
            orderItem.setAttribute('data-price', totalPrice.toFixed(2));
            orderList.appendChild(orderItem);

            // Add the item to the orderItems array
            orderItems.push({
                foodName: foodName,
                quantity: quantity,
                price: totalPrice.toFixed(2)
            });

            updateOrderSummary();
        } else {
            alert('Please select a food item and quantity.');
        }
    }

    addToOrderButton.addEventListener('click', addToOrder);

    // Handle form submission
    paymentForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Gather user details
        const userDetails = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            address: document.getElementById('address').value,
            phone: document.getElementById('phone').value,
        };

        // Gather payment method
        const paymentMethod = document.querySelector('input[name="payment-method"]:checked').value;

        // Prepare data to send to the server
        const orderData = {
            userDetails: userDetails,
            orderItems: orderItems,
            totalCost: totalCostSpan.textContent,
            paymentMethod: paymentMethod
        };

        // Send data to the backend using fetch
        fetch(paymentUrl, {  // Use the payment URL from the form
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Order placed successfully!');
                // Reset form and orderItems
                orderItems = [];
                orderList.innerHTML = '';
                totalCostSpan.textContent = '₹0.00';
                paymentForm.reset();  // Clears the form fields
            } else {
                alert('Failed to place the order.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
// JavaScript to handle image preview
document.getElementById('barcodeUpload').addEventListener('change', function(event) {
    const previewContainer = document.getElementById('imagePreview');
    const previewImage = previewContainer.querySelector('.preview-img');
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewContainer.style.display = 'block';
        }
        reader.readAsDataURL(file);
    } else {
        previewContainer.style.display = 'none';
        previewImage.src = '#';
    }
});
