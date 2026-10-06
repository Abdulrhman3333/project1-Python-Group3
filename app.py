from datetime import datetime

import streamlit as st

from core import PARKING_PRICE, Store

st.set_page_config(page_title="Riyadh events", page_icon="🎟️", layout="wide")

# ------------------------------------------------------------------
# 1. STYLE: Streamlit lets you inject CSS with st.markdown(unsafe_allow_html=True)
# ------------------------------------------------------------------
ACCENTS = {  # every event gets its own colour
    "Boulevard World": "#E4572E",
    "Comedy Show": "#A86B00",
    "Kingdom Arena Boxing Night": "#B3202B",
    "Winter Wonderland": "#2F6FED",
}

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Figtree:wght@400;500;600&display=swap');
html, body, .stApp { font-family: 'Figtree', sans-serif; }
h1, h2, h3 { font-family: 'Bricolage Grotesque', sans-serif !important; letter-spacing: -0.02em; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1100px; padding-top: 2.5rem; }

/* any container created with key="card_..." or key="row_..." becomes a white ticket */
[class*="st-key-card_"], [class*="st-key-row_"] {
    background: #fff; border-radius: 18px; padding: 1.1rem;
    box-shadow: 0 1px 0 #d5dbe4, 0 14px 28px -20px rgba(27,36,51,.45);
}
.stub { display: flex; align-items: center; gap: 1rem; }
.stub .date { width: 64px; text-align: center; border-radius: 12px; padding: .55rem 0;
              background: var(--accent); color: #fff; line-height: 1; }
.stub .date b { display: block; font: 800 1.7rem 'Bricolage Grotesque', sans-serif; }
.stub .date span { font-size: .78rem; font-weight: 600; }
.stub .info { flex: 1; }
.stub .info h3 { margin: 0; padding: 0; font-size: 1.25rem; }
.stub .info p { margin: .15rem 0 0; color: #5b6678; font-size: .9rem; }
.stub .price { text-align: right; font: 800 1.5rem 'Bricolage Grotesque', sans-serif; }
.stub .price small { display: block; font: 500 .75rem 'Figtree', sans-serif; color: #5b6678; }


.st-emotion-cache-s4bvyn.epcrwu50 {
    color: #d41a1a !important; 
}

.st-emotion-cache-1bpuen8.epcrwu50{
    color: #d41a1a !important; 
}


/* the perforated tear line, with a notch cut out on each side */
.perf { border-top: 2px dashed #cfd6e0; margin: 1rem -1.1rem; position: relative; }
.perf::before, .perf::after { content: ""; position: absolute; top: -11px; width: 20px; height: 20px;
                              border-radius: 50%; background: #E9EDF2; }
.perf::before { left: -10px; }
.perf::after { right: -10px; }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# 2. STATE: Streamlit re-runs this whole file on every click, so anything that
#    must survive (cart, stock...) lives in st.session_state.
# ------------------------------------------------------------------
if "store" not in st.session_state:
    st.session_state.store = Store()
store = st.session_state.store


# ------------------------------------------------------------------
# 3. ACTIONS: run as on_click callbacks, i.e. BEFORE the page is redrawn,
#    so the sidebar total is never one click behind.
# ------------------------------------------------------------------
def run(action, *args):
    ok, msg = action(*args)
    st.toast(msg, icon="✅" if ok else "⚠️")
    if ok and action.__name__ == "checkout":
        st.session_state.celebrate = True


def slug(event):
    return event.name.lower().replace(" ", "-")


if st.session_state.pop("celebrate", False):
    st.balloons()

# ------------------------------------------------------------------
# 4. LAYOUT
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Find an event")
    query = st.text_input("Search", placeholder="Try “comedy”", label_visibility="collapsed")
    st.divider()
    st.metric("Cart total", f"{store.cart_total()} SAR")

st.title("Riyadh events")
st.caption("Pick a night out, add parking, and check out in one step.")

tab_events, tab_cart, tab_bookings = st.tabs(["Events", "Cart", "My bookings"])

# ---------- Events ----------
with tab_events:
    visible = [e for e in store.events if query.strip().lower() in e.name.lower()]
    if not visible:
        st.info(f"No events match “{query}”. Clear the search to see all events.")

    cols = st.columns(2)
    for n, e in enumerate(visible):
        day = datetime.strptime(e.date, "%Y-%m-%d")
        sold_out = e.tickets_available == 0
        parking_left = e.parking_available()

        with cols[n % 2]:
            with st.container(key=f"card_{n}"):
                st.markdown(
                    f"""<div class="stub" style="--accent:{ACCENTS.get(e.name, '#1B2433')}">
<div class="date"><b>{day.day}</b><span>{day.strftime('%b')}</span></div>
<div class="info"><h3>{e.name}</h3><p>{e.location}, {e.time}</p></div>
<div class="price">{e.price}<small>SAR per ticket</small></div>
</div>
<div class="perf"></div>""",
                    unsafe_allow_html=True,
                )
                st.progress(
                    (e.tickets_total - e.tickets_available) / e.tickets_total,
                    text="Sold out" if sold_out else f"{e.tickets_available} of {e.tickets_total} tickets left",
                )
                st.button(
                    "Sold out" if sold_out else "Add ticket",
                    key=f"t_{slug(e)}",
                    type="primary",
                    width="stretch",
                    disabled=sold_out,
                    on_click=run,
                    args=(store.add_ticket, e),
                )
                c1, c2 = st.columns([1, 2], vertical_alignment="center")
                spots = c1.number_input(
                    "Spots", 1, max(parking_left, 1), 1,
                    key=f"ps_{slug(e)}_{parking_left}",  # key changes with stock -> no stale value
                    label_visibility="collapsed",
                )
                c2.button(
                    f"Add parking ({PARKING_PRICE} SAR each)",
                    key=f"p_{slug(e)}",
                    width="stretch",
                    disabled=parking_left == 0,
                    on_click=run,
                    args=(store.add_parking, e, spots),
                )
                st.caption(f"{parking_left} parking spots left")

# ---------- Cart ----------
with tab_cart:
    if not (store.cart or store.parking_cart):
        st.info("Your cart is empty. Add a ticket from the Events tab.")
    else:
        for item in store.cart:
            with st.container(key=f"row_t_{slug(item.event)}"):
                c = st.columns([5, 1, 1, 1, 1], vertical_alignment="center")
                c[0].markdown(f"**{item.event.name}**  \n{item.event.price} SAR × {item.tickets} = {item.total_price()} SAR")
                c[1].button("−", key=f"dec_{slug(item.event)}", on_click=run, args=(store.change_tickets, item.event, -1))
                c[2].markdown(f"<div style='text-align:center;font-weight:600'>{item.tickets}</div>", unsafe_allow_html=True)
                c[3].button("+", key=f"inc_{slug(item.event)}", on_click=run, args=(store.change_tickets, item.event, 1))
                c[4].button("Remove", key=f"rm_t_{slug(item.event)}", on_click=run, args=(store.remove_ticket, item.event))

        for item in store.parking_cart:
            with st.container(key=f"row_p_{slug(item.event)}"):
                c = st.columns([8, 1.3], vertical_alignment="center")
                c[0].markdown(f"**Parking, {item.event.name}**  \n{item.spots} spot(s) × {PARKING_PRICE} SAR = {item.total_price()} SAR")
                c[1].button("Remove", key=f"rm_p_{slug(item.event)}", on_click=run, args=(store.remove_parking, item.event))

        st.divider()
        left, right = st.columns([2, 1], vertical_alignment="center")
        left.metric("Total", f"{store.cart_total()} SAR")
        right.button("Check out", type="primary", width="stretch", on_click=run, args=(store.checkout,))

# ---------- My bookings ----------
with tab_bookings:
    if not (store.my_tickets or store.parking_reservations):
        st.info("No bookings yet. Tickets and parking appear here after checkout.")

    for t in store.my_tickets:
        with st.container(key=f"row_bt_{slug(t.event)}"):
            c = st.columns([5, 1.6], vertical_alignment="center")
            c[0].markdown(f"**{t.event.name}**  \n{t.event.date}, {t.tickets} ticket(s)")
            c[1].button("Sell 1 ticket", key=f"sell_{slug(t.event)}", on_click=run, args=(store.sell_ticket, t.event, 1))

    for p in store.parking_reservations:
        with st.container(key=f"row_bp_{slug(p.event)}"):
            c = st.columns([5, 1.6], vertical_alignment="center")
            c[0].markdown(f"**Parking, {p.event.name}**  \n{p.event.date}, {p.spots} spot(s)")
            c[1].button("Cancel 1 spot", key=f"cancel_{slug(p.event)}", on_click=run, args=(store.cancel_parking, p.event, 1))
