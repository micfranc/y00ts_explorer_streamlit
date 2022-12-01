import requests
import streamlit as st
import json
import time
import datetime

endpoint = st.sidebar.selectbox(
    "Endpoints", ["y00ts Overview", "Recently Sold", "Recently Listed"]
)
st.header(f"y00ts Explorer - {endpoint}")


if endpoint == "y00ts Overview":
    url_stats = requests.get(
        "https://api-mainnet.magiceden.dev/v2/collections/y00ts/stats"
    )
    stats_data = json.loads(url_stats.text)
    listedCount = stats_data["listedCount"]
    st.subheader(f"The listed count equals :{listedCount}")

    floorPrice = stats_data["floorPrice"]
    floorPrice = floorPrice / 1000000000
    st.subheader(f"The floor price equals :{floorPrice} SOL")
    st.image(
        "https://img-cdn.magiceden.dev/rs:fill:400:400:0:0/plain/https://bafkreidc5co72clgqor54gpugde6tr4otrubjfqanj4vx4ivjwxnhqgaai.ipfs.dweb.link/"
    )


if endpoint == "Recently Sold":
    # floor_price_selector = st.sidebar.selectbox("Floor Price?", ['Below Floor', 'Above Floor'])
    params = {"type": "buyNow"}
    url_listings = requests.get(
        "https://api-mainnet.magiceden.dev/v2/collections/y00ts/activities?offset=0&limit=1000",
        params=params,
    )

    listings_data = json.loads(url_listings.text)
    print(listings_data)
    # output_dict = [x for x in listings_data if x["type"] == "buyNow"]
    # print("return")
    # output_json = json.loads(output_dict.text)
    # print(output_json)

    url_stats = requests.get(
        "https://api-mainnet.magiceden.dev/v2/collections/y00ts/stats"
    )
    stats_data = json.loads(url_stats.text)

    floorPrice = stats_data["floorPrice"]
    floorPrice = floorPrice / 1000000000
    with st.sidebar:
        st.write(f"The floor price equals: {floorPrice} SOL")

    for yoot in listings_data:
        # "https://metadata.y00ts.com/y/12758.png"
        replace_1 = yoot["image"].replace("https://metadata.y00ts.com/y/", "")
        replace_2 = replace_1.replace(".png", "")
        st.subheader(f"y00t #{replace_2}")
        img_url = yoot["image"]
        mint_address = yoot["tokenMint"]
        st.image(img_url)
        price = int(yoot["price"])

        # print(price)
        # # st.write(f"Price of y00t: {price} SOL")
        sol_price = str(price) + " SOL"
        diff = round(price - floorPrice)

        title = "Sale price of y00t #" + replace_2
        # st.metric(label=title, value=sol_price, delta=diff, delta_color="inverse")

        if price > floorPrice:
            sol_diff = str(diff) + " SOL above floor price"
            st.metric(label=title, value=sol_price, delta=sol_diff)
        elif price == floorPrice:
            sol_diff = str(diff) + " SOL equals floor price"
            st.metric(label=title, value=sol_price, delta=sol_diff, delta_color="off")
        else:
            sol_diff = str(diff) + " SOL below floor price"
            st.metric(label=title, value=sol_price, delta=sol_diff)

        item_url = (
            f"https://magiceden.io/item-details/{mint_address}?name=y00t-%23{replace_2}"
        )
        st.write(item_url)

## RECENTLY LISTED

if endpoint == "Recently Listed":
    # floor_price_selector = st.sidebar.selectbox("Floor Price?", ['Below Floor', 'Above Floor'])
    url_listings = requests.get(
        "https://api-mainnet.magiceden.dev/v2/collections/y00ts/listings?offset=0&limit=20"
    )
    listings_data = json.loads(url_listings.text)

    url_stats = requests.get(
        "https://api-mainnet.magiceden.dev/v2/collections/y00ts/stats"
    )
    stats_data = json.loads(url_stats.text)

    floorPrice = stats_data["floorPrice"]
    floorPrice = floorPrice / 1000000000
    with st.sidebar:
        st.write(f"The floor price equals: {floorPrice} SOL")

    for yoot in listings_data:
        # "https://metadata.y00ts.com/y/11252.png"

        replace_1 = yoot["extra"]["img"].replace("https://metadata.y00ts.com/y/", "")
        replace_2 = replace_1.replace(".png", "")
        st.subheader(f"y00t #{replace_2}")
        img_url = yoot["extra"]["img"]
        mint_address = yoot["tokenMint"]
        # with st.container():
        #     for col in st.columns(4):
        #         col.image(img_url, width=150)
        st.image(img_url)
        price = int(yoot["price"])

        print(price)
        # st.write(f"Price of y00t: {price} SOL")
        diff = round(price - floorPrice)

        title = "y00t #" + replace_2
        sol_price = str(price) + " SOL"
        # st.metric(label=title, value=sol_price, delta=sol_diff, delta_color="inverse")

        if price > floorPrice:
            sol_diff = str(diff) + " SOL above floor price"
            st.metric(
                label=title, value=sol_price, delta=sol_diff, delta_color="inverse"
            )
        elif price == floorPrice:
            sol_diff = str(diff) + " SOL equals floor price"
            st.metric(label=title, value=sol_price, delta=sol_diff, delta_color="off")
        else:
            sol_diff = str(diff) + " SOL below floor price"
            st.metric(
                label=title, value=sol_price, delta=sol_diff, delta_color="inverse"
            )

        item_url = (
            f"https://magiceden.io/item-details/{mint_address}?name=y00t-%23{replace_2}"
        )
        # st.write(item_url)
        st.markdown(
            f"""<a href="https://magiceden.io/item-details/{mint_address}?name=y00t-%23{replace_2}">BUY NOW</a>""",
            unsafe_allow_html=True,
        )
