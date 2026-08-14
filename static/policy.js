document.addEventListener("DOMContentLoaded", function () {
  const searchBar = document.getElementById("searchBar");
  const policyCards = document.querySelectorAll(".policy-card");

  searchBar.addEventListener("input", function () {
    const query = searchBar.value.toLowerCase().trim();

    let anyVisible = false;

    policyCards.forEach(card => {
      const title = card.querySelector("h2").textContent.toLowerCase();
      const description = card.textContent.toLowerCase();

      if (title.includes(query) || description.includes(query)) {
        card.style.display = "block";
        anyVisible = true;
      } else {
        card.style.display = "none";
      }
    });

    // Optional: Show message if no results found
    let noResultMsg = document.getElementById("noResults");
    if (!noResultMsg) {
      noResultMsg = document.createElement("p");
      noResultMsg.id = "noResults";
      noResultMsg.style.textAlign = "center";
      noResultMsg.style.fontStyle = "italic";
      noResultMsg.style.color = "#888";
      document.getElementById("policyList").appendChild(noResultMsg);
    }

    noResultMsg.textContent = anyVisible ? "" : "No matching policy found.";
  });
});

