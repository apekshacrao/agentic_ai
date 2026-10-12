document.querySelectorAll("img").forEach((image) => {
  image.addEventListener("error", () => {
    image.src = "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1000&q=80";
  });
});
