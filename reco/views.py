from django.shortcuts import render
import pandas as pd
import joblib


def index(request):
    return render(request, 'reco/index.html')


def recommendation(request):
    dry = 0
    oil = 0
    product = request.POST.get('product')
    skin = request.POST.get('skin')
    if skin == 'Dry':
        dry = 1
    elif skin == 'Oily':
        oil = 1
    elif skin == 'Normal':
        oil, dry, normal = (1,1,1)

    recommendObj = recommend()

    columns = [{'field': f, 'title': f} for f in ["Name", "Brand", "Price", "Rank"]]

    jsonDataframed = recommendObj.get_recommendations(product,Dry = dry, Oily = oil).to_json(orient='records')

    context = {
        'data': jsonDataframed,
        'columns': columns
    }
    return render(request, 'reco/recommendation.html', context)


class recommend:

    def __init__(self):
        self.dataset = pd.read_csv('C:/Users/simon/Development/cosmetics/reco/datasets/cosmetics.csv')
        self.indices = pd.Series(self.dataset.index, index=self.dataset['Name']).drop_duplicates()
        self.cosine_sim = joblib.load('C:/Users/simon/Development/cosmetics/reco/model.file', )

    def get_recommendations(self, Name, Normal = 1, Dry=1, Oily=1 ):
        # Get the index of the products that matches the title
        idx = self.indices[Name]

        # Get the pairwsie similarity scores of all ingredient with that other ingredidnets
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # Sort the product based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the products indices
        product_indicies = [i[0] for i in sim_scores]

        product_sim = self.dataset.loc[product_indicies]
        dry_mask = product_sim['Dry'] == Dry
        normal_mask = product_sim['Normal'] == Normal
        oily_mask = product_sim['Oily'] == Oily
        recos = product_sim[dry_mask & normal_mask & oily_mask]
        recommendations = recos.copy()
        length = len(recommendations.values)
        recommendations['Rank'] = [x for x in range(1, length + 1)]
        recommendations = recommendations.reset_index(drop=True)
        # Return the top 10 most similar products
        return recommendations.loc[:, ["Name", "Brand", "Price", "Rank"]]
