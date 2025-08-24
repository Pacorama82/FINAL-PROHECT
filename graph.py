import collections

class Graph:
    """
    Represents a city map with both topological (edges) 
    and geometric (node coordinates) data.
    """
    def __init__(self):
        self.adjacency_list = collections.defaultdict(list)
        # This dictionary is the critical link between the two worlds
        self.node_coordinates = {}

    def load_map_data(self, filename):
        """
        Loads all map data from the single, unified 7-column CSV file.
        This method populates BOTH the adjacency_list and node_coordinates.
        """
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                
                parts = line.strip().split(',')
                start_id, start_x, start_y, end_id, end_x, end_y, weight = parts
                
                # Store the coordinates for both nodes
                self.node_coordinates[start_id] = (float(start_x), float(start_y))
                self.node_coordinates[end_id] = (float(end_x), float(end_y))
                
                # Store the edge for the undirected graph
                self.adjacency_list[start_id].append((end_id, float(weight)))
                self.adjacency_list[end_id].append((start_id, float(weight)))

    def find_nearest_vertex(self, point):
        return min(self.node_coordinates, key=lambda node_id:
                   (self.node_coordinates[node_id][0] - point[0])**2 +
                   (self.node_coordinates[node_id][1] - point[1])**2)

    def dijkstra(self, start, end):
        import heapq
        heap = [(0, start)]
        visited = set()
        while heap:
            cost, node = heapq.heappop(heap)
            if node == end:
                return cost
            if node in visited:
                continue
            visited.add(node)
            for neighbor, weight in self.adjacency_list[node]:
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + weight, neighbor))
        return float('inf')
