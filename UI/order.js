var productPrices = {};

$(function () {
    $.get(productListApiUrl, function (response) {
        productPrices = {};
        if (response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function (index, product) {
                options += '<option value="' + product.product_id + '">' + product.name + '</option>';
                productPrices[product.product_id] = Number(product.price_per_unit || 0);
            });

            $(".product-box .cart-product").empty().html(options);
        }
    });
});

$("#addMoreButton").click(function () {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);

    var lastRow = $(".product-box-extra .product-item").last();
    lastRow.find(".product-price").val('0.00');
    lastRow.find(".product-qty").val('1');
    lastRow.find(".product-total").val('0.00');

    var lastSelect = lastRow.find(".cart-product");
    lastSelect.empty().html($(".product-box .cart-product").html());
    calculateValue();
});

$(document).on("click", ".remove-row", function () {
    $(this).closest('.product-item').remove();
    calculateValue();
});

$(document).on("change", ".cart-product", function () {
    var product_id = $(this).val();
    var price = productPrices[product_id] || 0;

    $(this).closest('.product-item').find('.product-price').val(price.toFixed(2));
    calculateValue();
});

$(document).on("input change", ".product-qty", function () {
    calculateValue();
});

$("#saveOrder").on("click", function () {
    var formData = $("form").serializeArray();
    var requestPayload = {
        customer_name: null,
        total: null,
        order_details: []
    };

    for (var i = 0; i < formData.length; ++i) {
        var element = formData[i];
        var lastElement = null;

        switch (element.name) {
            case 'customerName':
                requestPayload.customer_name = element.value;
                break;
            case 'product_grand_total':
                requestPayload.total = element.value;
                break;
            case 'product':
                requestPayload.order_details.push({
                    product_id: element.value,
                    quantity: null,
                    total_price: null
                });
                break;
            case 'qty':
                lastElement = requestPayload.order_details[requestPayload.order_details.length - 1];
                if (lastElement) {
                    lastElement.quantity = element.value;
                }
                break;
            case 'item_total':
                lastElement = requestPayload.order_details[requestPayload.order_details.length - 1];
                if (lastElement) {
                    lastElement.total_price = element.value;
                }
                break;
        }
    }

    callApi("POST", orderSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});