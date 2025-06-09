const countdown = (elementId, targetDate) => {
  const el = document.getElementById(elementId);
  if (!el) return;

  const update = () => {
    const now = new Date();
    const diff = targetDate - now;
    if (diff <= 0) {
      el.textContent = "The event has started!";
      clearInterval(interval);
      return;
    }
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    const seconds = Math.floor((diff / 1000) % 60);

    el.textContent = `🚨 Hackathon closes in ${days}d ${hours}h ${minutes}m ${seconds}s`;
  };

  update();
  const interval = setInterval(update, 1000);
};

module.exports = countdown;
