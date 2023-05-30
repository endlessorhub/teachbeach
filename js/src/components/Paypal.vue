<template>
    <div class="paypal-button">
      <paypal-buttons
          :on-approve="onApprove"
          :create-order="createOrder"
          :on-shipping-change="onShippingChange"
          :on-error="onError"
          :style-object="style"
      />
    </div>
</template>
<script>


export default {
    computed: {
      createOrder: function () {
        return (data, actions) => {
          return actions.order.create({
            purchase_units: [
              {
                amount: {
                  value: "10",
                },
              },
            ],
          });
        }
      },
      onApprove: function () {
        return (data, actions) => {
          return actions.order.capture();
        }
      },
      onShippingChange: function () {
        return (data, actions) => {
          console.log(data.shipping_address);
          return actions.resolve();
        }
      },
      onError: function () {
        return (err) => {
          console.error(err);
        }
      },
      style: function () {
        return {
          shape: 'pill',
          color: 'gold',
          layout: 'horizontal',
          label: 'paypal',
          tagline: false
        }
      },
    },
}
</script>