(() => {
  // Log page events only. The demo message is submitted explicitly by the Test Message form.
  function logEvent(eventName) {
    fetch("/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event: eventName }),
      keepalive: true
    }).catch(() => {});
  }
  logEvent("PAGE_VIEW");
  const learnMore = document.getElementById("learn-more");
  if (learnMore) learnMore.addEventListener("click", () => logEvent("LEARN_MORE_CLICKED"));
})();
