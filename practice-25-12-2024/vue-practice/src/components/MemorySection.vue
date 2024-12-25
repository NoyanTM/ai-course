<script setup>
import { ref, onMounted } from 'vue';

const cards = ref([]);
const attempts = ref(0);
const matches = ref(0);
const flippedCards = ref([]);
const showAllCards = ref(false);
const message = ref("");

// Function to start or restart the game
const startGame = () => {
  message.value = ""; // Reset message
  const items = Array.from({ length: 6 }, () => 1); // 6 correct cards (value 1)
  const emptyItems = Array.from({ length: 19 }, () => 0); // 19 empty cards (value 0)
  const pairedItems = [...items, ...emptyItems]; // Combine 1s and 0s

  cards.value = pairedItems
    .map((content) => ({
      content,
      flipped: true, // Show all cards initially
      matched: false,
    }))
    .sort(() => Math.random() - 0.5); // Shuffle cards

  attempts.value = 0;
  matches.value = 0;
  flippedCards.value = [];
  showAllCards.value = true;

  // Cover all cards after 5 seconds
  setTimeout(() => {
    cards.value.forEach((card) => {
      card.flipped = false;
    });
    showAllCards.value = false;
  }, 5000);
};

const flipCard = (index) => {
  if (showAllCards.value) return; // Disable flipping while all cards are visible

  const card = cards.value[index];
  // Ignore if already flipped, matched, or two cards are being checked
  if (card.flipped || card.matched || flippedCards.value.length === 2) {
    return;
  }

  card.flipped = true; // Flip the card
  flippedCards.value.push(index);

  if (flippedCards.value.length === 2) {
    checkMatch();
  }
};

// Function to check for a match between flipped cards
const checkMatch = () => {
  const [firstIndex, secondIndex] = flippedCards.value;
  const firstCard = cards.value[firstIndex];
  const secondCard = cards.value[secondIndex];

  if (firstCard.content === 1 && secondCard.content === 1) {
    // Match only if both cards are 1
    firstCard.matched = true;
    secondCard.matched = true;
    matches.value++;
  } else {
    // Unflip cards after a short delay if no match
    setTimeout(() => {
      firstCard.flipped = false;
      secondCard.flipped = false;
    }, 1000);
  }

  attempts.value++;
  flippedCards.value = [];

  // Check if the player has won
  if (matches.value >= 6) {
    message.value = "Congratulations! You won the game!";
  }
};
  
// Initialize the game when the component is mounted
onMounted(() => {
  startGame();
});
</script>

<template>
  <div class="container">
    <h1>Memory Game</h1>
    <div class="d-flex justify-content-between align-items-center">
      <div>Attempts: {{ attempts }}</div>
      <button class="btn btn-primary" @click="startGame">Restart</button>
      <div>Matches: {{ matches }}/6</div>
    </div>
    <p class="text-success mt-3">{{ message }}</p>
    <div class="row gap-3 mt-4">
      <div v-for="(card, index) in cards" :key="index" class="col-2">
        <div
          class="card border text-center items-center"
          :class="{
            'bg-light text-dark': !card.flipped && !card.matched,
            'bg-primary text-white': card.flipped && !card.matched,
            'bg-success text-white': card.matched,
          }"
          @click="flipCard(index)"
          style="width: 5rem; height: 5rem;"
        >
          <div v-if="card.flipped || card.matched">
            {{ card.content }}
          </div>
          <div v-else>
            ?
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


// const cards = ref([
//     {
//         id: 1,
//         is_active: true,
//     },
// ])

// rewrite game from random unique items to just binary (0 and 1, 1 is correct value and 0 is empty one), also fix game restart