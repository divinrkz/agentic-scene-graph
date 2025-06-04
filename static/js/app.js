// const form = document.getElementById("layoutForm");
// form.onsubmit = async (e) => {
//     e.preventDefault();
//     const params = new URLSearchParams(new FormData(form)).toString();
//     const response = await fetch(`/generate_layout?${params}`);
//     const html = await response.text();
//     document.getElementById("layoutResult").innerHTML = html;
// };

function addFurniture() {
    const container = document.getElementById("furnitureList");
    const item = document.createElement("div");
    item.className = "furnitureItem";
    item.innerHTML = `
      <input type="text" placeholder="Name" class="furnitureName" required>
      <div class="dimensions">
      <input type="number" step="0.1" placeholder="Width" class="furnitureWidth" required>
      <input type="number" step="0.1" placeholder="Length" class="furnitureLength" required>
      <input type="number" step="0.1" placeholder="Height" class="furnitureHeight" required>
      </div>
      <button type="button" class="removeFurnitureBtn">Remove</button>
    `;
    item.querySelector('.removeFurnitureBtn').onclick = () => {
      container.removeChild(item);
    };
    container.appendChild(item);
  }
  
  
  document.getElementById("layoutForm").onsubmit = async (e) => {
    e.preventDefault();
  
    const spaceType = document.getElementById("spaceType").value;
    const width = e.target.width.value;
    const height = e.target.height.value;
    const length = e.target.length.value;
  
    const furnitureItems = [];
    document.querySelectorAll(".furnitureItem").forEach(item => {
      const name = item.querySelector(".furnitureName").value;
      const w = parseFloat(item.querySelector(".furnitureWidth").value);
      const l = parseFloat(item.querySelector(".furnitureLength").value);
      const h = parseFloat(item.querySelector(".furnitureHeight").value);
      furnitureItems.push({ name, dimensions: [w, l, h] });
    });
  
    const response = await fetch("/generate_layout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        spaceType,
        width,
        height,
        length,
        furnitureCatalog: furnitureItems
      })
    });
  
    const html = await response.text();
    document.getElementById("layoutResult").innerHTML = html;
  };
  