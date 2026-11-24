const currency = new Intl.NumberFormat("es", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const salesCategory = document.querySelector("#sales-category");
const salesRegion = document.querySelector("#sales-region");
const salesStatus = document.querySelector("#sales-status");
let salesData = [];

function formatCurrency(value) {
  return currency.format(value);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

async function loadSales() {
  try {
    const response = await fetch("data/ventas.csv");
    if (!response.ok) {
      throw new Error(`No se pudo cargar el CSV (HTTP ${response.status}).`);
    }
    const [headerLine, ...lines] = (await response.text()).trim().split(/\r?\n/);
    const columns = headerLine.split(",");
    const required = ["venta_id", "fecha", "producto", "categoria", "region", "unidades", "precio_unitario"];
    if (required.some((column) => !columns.includes(column))) {
      throw new Error("El CSV no contiene todas las columnas esperadas.");
    }
    const indexes = Object.fromEntries(required.map((column) => [column, columns.indexOf(column)]));
    salesData = lines.map((line) => {
      const values = line.split(",");
      const units = Number(values[indexes.unidades]);
      const price = Number(values[indexes.precio_unitario]);
      return {
        id: values[indexes.venta_id],
        date: values[indexes.fecha],
        product: values[indexes.producto],
        category: values[indexes.categoria],
        region: values[indexes.region],
        units,
        revenue: units * price,
      };
    }).filter((sale) => sale.id && sale.date && sale.category && sale.region && sale.units > 0 && Number.isFinite(sale.revenue));
    if (salesData.length === 0) {
      throw new Error("El CSV no contiene filas válidas para mostrar.");
    }
    populateFilters();
    renderSales();
    salesStatus.textContent = `${salesData.length} transacciones cargadas · conjunto sintético de demostración.`;
  } catch (error) {
    salesStatus.textContent = `No fue posible cargar el dashboard: ${error.message}`;
  }
}

function populateFilters() {
  for (const [select, key] of [[salesCategory, "category"], [salesRegion, "region"]]) {
    const values = [...new Set(salesData.map((sale) => sale[key]))].sort();
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.append(option);
    }
  }
}

function renderSales() {
  const filtered = salesData.filter((sale) =>
    (salesCategory.value === "all" || sale.category === salesCategory.value)
    && (salesRegion.value === "all" || sale.region === salesRegion.value));
  const total = filtered.reduce((sum, sale) => sum + sale.revenue, 0);
  const orders = new Set(filtered.map((sale) => sale.id)).size;
  const units = filtered.reduce((sum, sale) => sum + sale.units, 0);
  document.querySelector("#metric-revenue").textContent = formatCurrency(total);
  document.querySelector("#metric-orders").textContent = String(orders);
  document.querySelector("#metric-units").textContent = String(units);
  document.querySelector("#metric-average").textContent = formatCurrency(orders ? total / orders : 0);

  const monthly = new Map();
  const categories = new Map();
  for (const sale of filtered) {
    const month = sale.date.slice(0, 7);
    monthly.set(month, (monthly.get(month) || 0) + sale.revenue);
    categories.set(sale.category, (categories.get(sale.category) || 0) + sale.revenue);
  }
  renderMonthlyChart(monthly);
  renderCategoryChart(categories);
}

function renderMonthlyChart(monthly) {
  const chart = document.querySelector("#monthly-chart");
  chart.replaceChildren();
  const values = [...monthly.entries()].sort(([a], [b]) => a.localeCompare(b));
  const max = Math.max(...values.map(([, value]) => value), 1);
  for (const [month, value] of values) {
    const column = document.createElement("div");
    column.className = "bar-column";
    const bar = document.createElement("i");
    bar.style.height = `${Math.max(3, (value / max) * 100)}%`;
    bar.title = `${month}: ${formatCurrency(value)}`;
    const label = document.createElement("span");
    label.textContent = month.slice(5);
    column.append(bar, label);
    chart.append(column);
  }
}

function renderCategoryChart(categories) {
  const chart = document.querySelector("#category-chart");
  chart.replaceChildren();
  const values = [...categories.entries()].sort(([, a], [, b]) => b - a);
  const max = Math.max(...values.map(([, value]) => value), 1);
  for (const [name, value] of values) {
    const row = document.createElement("div");
    row.className = "horizontal-row";
    const label = document.createElement("span");
    label.textContent = name;
    const track = document.createElement("div");
    track.className = "horizontal-track";
    const bar = document.createElement("i");
    bar.style.width = `${(value / max) * 100}%`;
    track.append(bar);
    const amount = document.createElement("strong");
    amount.textContent = formatCurrency(value);
    row.append(label, track, amount);
    chart.append(row);
  }
}

salesCategory.addEventListener("change", renderSales);
salesRegion.addEventListener("change", renderSales);
loadSales();

const expenses = [
  { description: "Almuerzo", category: "Comida", amount: 12.5 },
  { description: "Bus", category: "Transporte", amount: 2.25 },
  { description: "Café", category: "Comida", amount: 3.75 },
];

function renderExpenses() {
  const total = expenses.reduce((sum, expense) => sum + expense.amount, 0);
  document.querySelector("#expense-total").textContent = formatCurrency(total);
  const list = document.querySelector("#expense-list");
  list.replaceChildren();
  for (const expense of expenses.slice(-4).reverse()) {
    const row = document.createElement("div");
    row.className = "list-row";
    const detail = document.createElement("span");
    detail.innerHTML = `${escapeHtml(expense.description)}<small>${escapeHtml(expense.category)}</small>`;
    const amount = document.createElement("strong");
    amount.textContent = formatCurrency(expense.amount);
    row.append(detail, amount);
    list.append(row);
  }
}

document.querySelector("#expense-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = new FormData(form);
  const amount = Number(values.get("amount"));
  const category = String(values.get("category")).trim();
  const description = String(values.get("description")).trim();
  if (!Number.isFinite(amount) || amount <= 0 || !category || !description) {
    form.reportValidity();
    return;
  }
  expenses.push({ description, category, amount });
  renderExpenses();
  form.reset();
});
renderExpenses();

const weatherForm = document.querySelector("#weather-form");
const weatherStatus = document.querySelector("#weather-status");
const weatherResult = document.querySelector("#weather-result");

weatherForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = document.querySelector("#weather-city").value.trim();
  if (!city) {
    weatherStatus.textContent = "Escribe el nombre de una ciudad.";
    return;
  }
  weatherStatus.textContent = "Consultando Open-Meteo…";
  weatherResult.replaceChildren();
  try {
    const geocodingUrl = new URL("https://geocoding-api.open-meteo.com/v1/search");
    geocodingUrl.search = new URLSearchParams({ name: city, count: "1", language: "es", format: "json" });
    const locationResponse = await fetch(geocodingUrl);
    if (!locationResponse.ok) throw new Error("No se pudo buscar esa ciudad.");
    const locationData = await locationResponse.json();
    const location = locationData.results?.[0];
    if (!location) throw new Error(`No se encontró la ciudad «${city}».`);

    const forecastUrl = new URL("https://api.open-meteo.com/v1/forecast");
    forecastUrl.search = new URLSearchParams({
      latitude: String(location.latitude),
      longitude: String(location.longitude),
      current: "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m",
      timezone: "auto",
    });
    const forecastResponse = await fetch(forecastUrl);
    if (!forecastResponse.ok) throw new Error("No se pudo consultar el pronóstico.");
    const { current } = await forecastResponse.json();
    if (!current) throw new Error("La respuesta del servicio no incluye el clima actual.");

    const place = [location.name, location.admin1, location.country].filter(Boolean).join(", ");
    const title = document.createElement("p");
    title.className = "weather-place";
    title.textContent = place;
    const temperature = document.createElement("p");
    temperature.className = "weather-temp";
    temperature.textContent = `${current.temperature_2m}°`;
    const details = document.createElement("div");
    details.className = "weather-details";
    details.textContent = `Sensación ${current.apparent_temperature}° · Humedad ${current.relative_humidity_2m}% · Viento ${current.wind_speed_10m} km/h`;
    weatherResult.append(title, temperature, details);
    weatherStatus.textContent = `Actualizado: ${current.time || "ahora"}.`;
  } catch (error) {
    weatherStatus.textContent = `Error: ${error.message}`;
  }
});

const books = [
  { title: "El principito", author: "Antoine de Saint-Exupéry", year: 1943 },
  { title: "Cien años de soledad", author: "Gabriel García Márquez", year: 1967 },
];
const bookSearch = document.querySelector("#book-search");

function renderBooks() {
  const query = bookSearch.value.trim().toLocaleLowerCase("es");
  const matches = books.filter((book) =>
    `${book.title} ${book.author}`.toLocaleLowerCase("es").includes(query));
  const list = document.querySelector("#book-list");
  list.replaceChildren();
  for (const book of matches) {
    const row = document.createElement("div");
    row.className = "list-row";
    const detail = document.createElement("span");
    detail.innerHTML = `${escapeHtml(book.title)}<small>${escapeHtml(book.author)}</small>`;
    const year = document.createElement("strong");
    year.textContent = String(book.year);
    const remove = document.createElement("button");
    remove.className = "remove-book";
    remove.type = "button";
    remove.textContent = "Eliminar";
    remove.setAttribute("aria-label", `Eliminar ${book.title}`);
    remove.addEventListener("click", () => {
      books.splice(books.indexOf(book), 1);
      renderBooks();
    });
    row.append(detail, year, remove);
    list.append(row);
  }
  if (matches.length === 0) {
    const empty = document.createElement("p");
    empty.className = "demo-note";
    empty.textContent = "No se encontraron libros.";
    list.append(empty);
  }
}

bookSearch.addEventListener("input", renderBooks);
document.querySelector("#book-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = new FormData(form);
  const title = String(values.get("title")).trim();
  const author = String(values.get("author")).trim();
  const year = Number(values.get("year"));
  if (!title || !author || !Number.isInteger(year) || year < 0 || year > 2100) {
    form.reportValidity();
    return;
  }
  books.push({ title, author, year });
  form.reset();
  renderBooks();
});
renderBooks();
