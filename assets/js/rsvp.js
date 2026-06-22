// RSVP form — progressive enhancement over a plain Web3Forms POST.
// No user input is ever written to the DOM as HTML (textContent only) → no XSS surface.
(function () {
  "use strict";
  var form = document.getElementById("rsvp-form");
  if (!form) return;

  var list = document.getElementById("guest-list");
  var addBtn = document.getElementById("add-guest");
  var status = document.getElementById("rsvp-status");
  var success = document.getElementById("rsvp-success");
  var MAX = 12;
  var seq = 1; // monotonic, so guest field names never collide after add/remove

  function setStatus(msg, state) {
    status.textContent = msg;
    status.className = "rsvp__status" + (state ? " is-" + state : "");
  }

  function guestCount() { return list.querySelectorAll(".guest-input").length; }
  function syncAddBtn() { if (addBtn) addBtn.style.display = guestCount() >= MAX ? "none" : ""; }

  // Add another guest name field
  if (addBtn) {
    addBtn.addEventListener("click", function () {
      if (guestCount() >= MAX) return;

      var row = document.createElement("div");
      row.className = "guest-row";

      var input = document.createElement("input");
      input.type = "text";
      input.className = "rsvp__input guest-input";
      seq++;
      input.name = "Invité " + seq;
      input.maxLength = 80;
      input.placeholder = "Prénom et nom";
      input.autocomplete = "name";

      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "rsvp__remove";
      remove.setAttribute("aria-label", "Retirer cet invité");
      remove.textContent = "×";
      remove.addEventListener("click", function () { row.remove(); syncAddBtn(); });

      row.appendChild(input);
      row.appendChild(remove);
      list.appendChild(row);
      input.focus();
      syncAddBtn();
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Honeypot: a real user never checks this hidden box.
    if (form.botcheck && form.botcheck.checked) return;

    var key = form.access_key.value;
    if (!key || key.indexOf("PLACEHOLDER") === 0) {
      setStatus("Le formulaire en ligne sera activé très bientôt. En attendant, merci de confirmer directement auprès des mariés ou de leurs parents.", "err");
      return;
    }

    var guests = [];
    form.querySelectorAll(".guest-input").forEach(function (i) {
      var v = i.value.trim();
      if (v) guests.push(v);
    });
    if (guests.length === 0) {
      setStatus("Merci d’indiquer au moins un nom.", "err");
      return;
    }

    var presenceEl = form.querySelector('input[name="Présence"]:checked');
    var payload = {
      access_key: key,
      subject: form.subject.value,
      from_name: form.from_name.value,
      "Présence": presenceEl ? presenceEl.value : "",
      "Invité(s)": guests.join(", "),
      "Nombre d'invités": guests.length,
      "Message": form.Message.value.trim(),
      botcheck: false
    };

    var submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;
    setStatus("Envoi en cours…", "pending");

    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data && data.success) {
          // Show the confirmation panel in place of the form.
          form.reset();
          form.style.display = "none";
          setStatus("", null);
          if (success) {
            success.hidden = false;
            success.scrollIntoView({ behavior: "smooth", block: "center" });
          }
        } else {
          setStatus("Une erreur est survenue. Merci de réessayer ou de nous répondre directement.", "err");
          if (submitBtn) submitBtn.disabled = false;
        }
      })
      .catch(function () {
        setStatus("Connexion impossible. Merci de réessayer ou de nous répondre directement.", "err");
        if (submitBtn) submitBtn.disabled = false;
      });
  });
})();
