<script setup>
import { ref, computed } from 'vue';

const basket = ref([
    {
        id: 1,
        name: 'Product 1',
        price: 100,
        quantity: 1
    },
    {
        id: 2,
        name: 'Product 2',
        price: 200,
        quantity: 2
    },
    {
        id: 3,
        name: 'Product 3',
        price: 300,
        quantity: 3
    },
    {
        id: 4,
        name: 'Product 4',
        price: 400,
        quantity: 4
    }
])

function increaseQuantity(index) {
    this.basket[index].quantity++;
}

function decreaseQuantity(index) {
    if (this.basket[index].quantity > 0) {
        this.basket[index].quantity--;
    }
}

const total = computed(() => {
    let totalValue = 0;
    for (let i = 0; i < basket.value.length; i++) {
        totalValue += basket.value[i].price * basket.value[i].quantity;
    }
    return totalValue;
});
</script>

<template>
    <div class="container">
        <div v-for="(item, index) in basket" class="basket-item">
            <div class="basket-item-text">
                <h2>{{ item.id }}</h2>
                <p>Price: {{ item.price }}</p>
                <p>Quantity: {{ item.value.quantity }}</p>
                <p>Sum: {{ item.price * item.quantity }}</p>
            </div>
        </div>
    </div>
</template>

<!-- {/* <div class="basket-item-buttons">
    <button type="submit" class="btn btn-primary btn-block btn-large" @click="increaseQuantity(index)">+</button>
    <button type="submit" class="btn btn-primary btn-block btn-large" @click="decreaseQuantity(index)">-</button>
</div> */} -->