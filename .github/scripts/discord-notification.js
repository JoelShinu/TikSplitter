const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
  ],
});

client.once('ready', () => {
  console.log('Discord bot is ready!');
});

client.login(process.env.DISCORD_TOKEN);

client.on('messageCreate', (message) => {
  if (message.channel.id === process.env.DISCORD_CHANNEL_ID) {
    message.channel.send('New PR: ' + message.content);
  }
});