import numpy as np
from sklearn.cluster import KMeans

from plugIn.processing_weight.allocationBase import AllocationBase


class ClusteredAllocator(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=100000, short_ratio=None, n_clusters=3):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)
        self.n_clusters = n_clusters

    def get_allocation(self):
        try:
            # Convert weights and prices from dicts to arrays
            tickers = list(self.weights.keys())
            weights_array = np.array([self.weights[ticker] for ticker in tickers])
            prices_array = np.array([self.latest_prices[ticker] for ticker in tickers])

            # Perform clustering based on asset similarity
            kmeans = KMeans(n_clusters=self.n_clusters, random_state=0)
            asset_features = np.column_stack((weights_array, prices_array))  # Use weights and prices as features
            clusters = kmeans.fit_predict(asset_features)

            # Allocate portfolio value to each cluster
            cluster_weights = np.array([
                np.sum(weights_array[clusters == i]) for i in range(self.n_clusters)
            ])
            cluster_allocation = (cluster_weights / np.sum(cluster_weights)) * self.total_portfolio_value

            # Within each cluster, allocate based on original weights
            allocation = {ticker: 0 for ticker in tickers}
            total_allocated_value = 0

            for i in range(self.n_clusters):
                cluster_assets = np.where(clusters == i)[0]
                cluster_value = cluster_allocation[i]
                cluster_weights_sum = np.sum(weights_array[cluster_assets])

                for asset_idx in cluster_assets:
                    ticker = tickers[asset_idx]
                    share_count = np.floor(
                        (weights_array[asset_idx] / cluster_weights_sum) * cluster_value / prices_array[asset_idx]
                    ).astype(int)
                    allocation[ticker] += share_count
                    total_allocated_value += share_count * prices_array[asset_idx]

            # Calculate remaining budget
            remaining_budget = self.total_portfolio_value - total_allocated_value

            return allocation, remaining_budget

        except Exception as ex:
            return {"error": str(ex)}, 0
