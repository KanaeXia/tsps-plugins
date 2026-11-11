function greet({ player }) {
  player.sendMessage("Welcome to the world. Enjoy your adventure!");
}

module.exports = {
  name: "WelcomeMessage",
  register(api) {
    api.onPlayerLogin(greet);
  },
};
