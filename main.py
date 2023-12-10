import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objs as go

st.set_page_config(layout='wide')

main_df = pd.read_csv('zara_modified.csv')
ss = st.session_state
col1, col2 = st.columns([1, 6])

with col1:
    slider = st.slider('Slide to change the year:', min_value=2018, max_value=2022)

with col2:
    col2_1, col2_2, col2_3 = st.columns(3, gap='medium')

    with col2_1:
        st.subheader(f'Sale in {slider}')
        line_df = main_df.copy()
        line_df = line_df.groupby(['year_of_sale', 'month_of_sale'])['revenue'].sum().reset_index()
        line_df = line_df.loc[line_df['year_of_sale'] == slider]
        line_df = line_df.sort_values(by=['year_of_sale', 'month_of_sale'])
        # st.dataframe(line_df)
        visual = px.line(
            line_df,
            x='month_of_sale',
            y='revenue',
            labels={'month_of_sale': 'Month',
                    'revenue': 'Sale',
                    }
        )

        st.plotly_chart(visual, use_container_width=True)

    with col2_2:
        st.subheader(f'Sale by categories in {slider}')
        bar_df = main_df.copy()
        bar_df = bar_df.groupby(['category', 'age_group', 'gender', 'year_of_sale'])['revenue'].sum().reset_index()
        bar_df = bar_df.sort_values(by=['category', 'age_group', 'category'])
        bar_df = bar_df.loc[bar_df['year_of_sale'] == slider]

        visual = px.bar(
            bar_df,
            x='category',
            y='revenue',
            color='age_group',
            # facet_row='age_group',
            barmode='stack',
            labels={
                'category': 'Category',
                'revenue': 'Sale',
                'age_group': 'Age Group',
                # 'gender': 'Gender',

            }
        )

        st.plotly_chart(visual, use_container_width=True)

    with col2_3:
        st.subheader(f'Rating in {slider}')
        name_color_mat = st.selectbox('Types', ['Product', 'Color', 'Material'])
        scatter_df = main_df.copy()

        if name_color_mat == 'Product':
            scatter_df = scatter_df.groupby(['product_name', 'year_of_sale'])['average_rating'].mean().reset_index()

        elif name_color_mat == 'Color':
            scatter_df = scatter_df.groupby(['color', 'year_of_sale'])['average_rating'].mean().reset_index()

        elif name_color_mat == 'Material':
            scatter_df = scatter_df.groupby(['material', 'year_of_sale'])['average_rating'].mean().reset_index()

        scatter_df = scatter_df.sort_values(by='average_rating')
        scatter_df = scatter_df.loc[scatter_df['year_of_sale'] == slider]
        tmp = {'Product': 'product_name', 'Color': 'color', 'Material': 'material'}

        visual = px.scatter(
            scatter_df,
            x=tmp[name_color_mat],
            y='average_rating',
            labels={
                tmp[name_color_mat]: name_color_mat,
                'average_rating': 'Rating'
            }
        )

        st.plotly_chart(visual, use_container_width=True)

    col2_4, col2_5, col2_6 = st.columns(3, gap='medium')

    with col2_4:
        st.subheader(f'Impact of price and discount on sale in {slider}')
        bubble_df = main_df.copy()
        bubble_df['price'] = bubble_df['price'].round(0)
        bubble_df = bubble_df.groupby(['year_of_sale', 'price', 'discount'])['sales_count'].sum().reset_index()
        bubble_df = bubble_df.sort_values(by=['sales_count', 'price'])
        bubble_df = bubble_df.loc[bubble_df['year_of_sale'] == slider]

        visual = px.scatter(
            bubble_df,
            x='price',
            y='sales_count',
            size='discount',
            labels={
                'price': 'Price',
                'sales_count': 'Sale Count'
            }
        )

        st.plotly_chart(visual, use_container_width=True)

    with col2_5:
        st.subheader(f'Demographic distribution in {slider}')
        pyra_df = main_df.copy()
        pyra_df = pyra_df.groupby(['gender', 'age_group','year_of_sale'])['product_id'].count().reset_index()
        pyra_df = pyra_df.loc[pyra_df['year_of_sale'] == slider]
        pyra_df['percent'] = (pyra_df['product_id'] * 1.0 / sum(pyra_df['product_id'])) * 100

        y = pyra_df['age_group']
        x1 = pyra_df.loc[pyra_df['gender'] == 'Male']
        x2 = pyra_df.loc[pyra_df['gender'] == 'Female']
        x2['percent'] *= -1

        visual = go.Figure()
        visual.add_trace(go.Bar(
            y=y,
            x=x1['percent'],
            name='Male',
            orientation='h'
        ))

        visual.add_trace(go.Bar(
            y=y,
            x=x2['percent'],
            name='Female',
            orientation='h'
        ))

        visual.update_layout(
            barmode='relative',
            bargap=0.0,
            bargroupgap=0,
            xaxis=dict(
                tickvals=[-100, -20, -15, - 10, -5, 0, 5, 10, 15, 20, 100],
                ticktext=['100%', '20%', '15%', '10%', '5%', '0%',
                          '5%', '10%', '15%', '20%','100%'],
                title='Population in %'
            ),
        )

        st.plotly_chart(visual, use_container_width=True)

    with col2_6:
        st.subheader(f'Seasonal sales in {slider}')
        heat_df = main_df.copy()
        heat_df = heat_df.loc[heat_df['year_of_sale'] == slider]
        heat_df = heat_df.sort_values(by=['year_of_sale', 'month_of_sale', 'category'])
        heatmap_df = heat_df.pivot_table(index='category', columns=['year_of_sale', 'month_of_sale'],
                                         values='sales_count', fill_value=0)

        visual = px.imshow(
            heatmap_df,
            x=heatmap_df.columns.levels[1],
            y=heatmap_df.index,
            labels=dict(y="Category", x="Month", color="Sales Count"),
        )

        st.plotly_chart(visual, use_container_width=True)

