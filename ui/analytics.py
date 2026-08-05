import streamlit as st
import plotly.express as px


def show_analytics(analytics, cluster):

    st.title("📊 Movie Analytics Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🎬 Total Movies",
            analytics.total_movies()
        )

    with col2:
        st.metric(
            "⭐ Average Rating",
            analytics.average_rating()
        )

    st.divider()

    st.subheader("⭐ Top Rated Movies")

    st.dataframe(
        analytics.top_movies(),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📈 Rating Distribution")

    fig = px.histogram(
        x=analytics.ratings(),
        nbins=20,
        labels={
            "x": "Rating",
            "y": "Movies"
        },
        title="Distribution of Movie Ratings"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🎭 Top 10 Genres")

    genre_counts = analytics.genre_counts().head(10)

    genre_fig = px.bar(
        x=genre_counts.index,
        y=genre_counts.values,
        labels={
            "x": "Genre",
            "y": "Movies"
        },
        title="Top 10 Movie Genres"
    )

    st.plotly_chart(
        genre_fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("📅 Movies Released Per Year")

    release_data = analytics.release_years()

    release_fig = px.line(
        x=release_data.index,
        y=release_data.values,
        labels={
            "x": "Year",
            "y": "Movies Released"
        },
        title="Movie Release Trend"
    )

    st.plotly_chart(
        release_fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🤖 K-Means Cluster Distribution")

    cluster_counts = cluster.cluster_counts()

    cluster_fig = px.bar(
        x=cluster_counts.index.astype(str),
        y=cluster_counts.values,
        labels={
            "x": "Cluster",
            "y": "Number of Movies"
        },
        title="Movies per Cluster",
        color=cluster_counts.values,
        color_continuous_scale="viridis"
    )

    st.plotly_chart(
        cluster_fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🔍 Explore Movies in a Cluster")

    selected_cluster = st.selectbox(
        "Select Cluster",
        sorted(cluster_counts.index)
    )

    cluster_movies = cluster.movies_in_cluster(
        selected_cluster
    )

    st.dataframe(
        cluster_movies,
        use_container_width=True,
        hide_index=True
    )