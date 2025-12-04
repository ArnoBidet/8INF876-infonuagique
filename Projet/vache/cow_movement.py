import math
import random
from typing import List, Tuple, Dict

class Vector2D:
    """Simple 2D vector class for movement calculations"""
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)
    
    def limit(self, max_force):
        if self.magnitude() > max_force:
            return self.normalize() * max_force
        return self

class Cow:
    """Represents a cow with flocking behavior"""
    def __init__(self, cow_id: str, lat: float, lng: float):
        self.id = cow_id
        self.position = Vector2D(lat, lng)
        self.velocity = Vector2D(random.uniform(-0.0001, 0.0001), random.uniform(-0.0001, 0.0001))
        self.acceleration = Vector2D(0, 0)
        
        # Flocking parameters
        self.max_speed = 0.0002  # Maximum speed in lat/lng units
        self.max_force = 0.00005  # Maximum steering force
        self.perception_radius = 0.005  # How far the cow can "see" neighbors
        self.separation_radius = 0.002  # Minimum distance from neighbors
        
        # Zone management - start inside zone
        self.outside_zone = False
        self.return_force_strength = 0.0001  # Strength of return force when outside
        
        # Movement state
        self.wandering_angle = random.uniform(0, 2 * math.pi)
        self.wander_strength = 0.00002
        
    def distance_to(self, other_cow) -> float:
        """Calculate distance to another cow"""
        dx = self.position.x - other_cow.position.x
        dy = self.position.y - other_cow.position.y
        return math.sqrt(dx**2 + dy**2)
    
    def separation(self, neighbors: List['Cow']) -> Vector2D:
        """Steer to avoid crowding local flockmates"""
        steer = Vector2D(0, 0)
        count = 0
        
        for neighbor in neighbors:
            distance = self.distance_to(neighbor)
            if distance > 0 and distance < self.separation_radius:
                diff = self.position - neighbor.position
                diff = diff.normalize()
                diff = diff * (1.0 / distance)  # Weight by distance
                steer = steer + diff
                count += 1
        
        if count > 0:
            steer = steer * (1.0 / count)
            steer = steer.normalize() * self.max_speed
            steer = steer - self.velocity
            steer = steer.limit(self.max_force)
        
        return steer
    
    def alignment(self, neighbors: List['Cow']) -> Vector2D:
        """Steer towards the average heading of neighbors"""
        sum_velocity = Vector2D(0, 0)
        count = 0
        
        for neighbor in neighbors:
            if self.distance_to(neighbor) < self.perception_radius:
                sum_velocity = sum_velocity + neighbor.velocity
                count += 1
        
        if count > 0:
            sum_velocity = sum_velocity * (1.0 / count)
            sum_velocity = sum_velocity.normalize() * self.max_speed
            steer = sum_velocity - self.velocity
            steer = steer.limit(self.max_force)
            return steer
        
        return Vector2D(0, 0)
    
    def cohesion(self, neighbors: List['Cow']) -> Vector2D:
        """Steer to move toward the average position of neighbors"""
        sum_position = Vector2D(0, 0)
        count = 0
        
        for neighbor in neighbors:
            if self.distance_to(neighbor) < self.perception_radius:
                sum_position = sum_position + neighbor.position
                count += 1
        
        if count > 0:
            sum_position = sum_position * (1.0 / count)
            return self.seek(sum_position)
        
        return Vector2D(0, 0)
    
    def seek(self, target: Vector2D) -> Vector2D:
        """Steer towards a target"""
        desired = target - self.position
        desired = desired.normalize() * self.max_speed
        
        steer = desired - self.velocity
        steer = steer.limit(self.max_force)
        return steer
    
    def wander(self) -> Vector2D:
        """Random wandering behavior"""
        self.wandering_angle += random.uniform(-0.3, 0.3)
        
        wander_force = Vector2D(
            math.cos(self.wandering_angle) * self.wander_strength,
            math.sin(self.wandering_angle) * self.wander_strength
        )
        return wander_force
    
    def return_to_zone(self, zone_center: Vector2D) -> Vector2D:
        """Force to return to zone when outside"""
        if self.outside_zone:
            return_force = self.seek(zone_center)
            return return_force * 2.0  # Stronger force to return
        return Vector2D(0, 0)
    
    def flock(self, neighbors: List['Cow'], zone_center: Vector2D = None) -> None:
        """Main flocking behavior combining all forces"""
        sep = self.separation(neighbors) * 1.5
        ali = self.alignment(neighbors) * 1.0
        coh = self.cohesion(neighbors) * 1.0
        wan = self.wander() * 0.8
        
        # Apply forces
        self.acceleration = sep + ali + coh + wan
        
        # Add zone return force if outside
        if zone_center and self.outside_zone:
            zone_force = self.return_to_zone(zone_center)
            self.acceleration = self.acceleration + zone_force
    
    def update(self) -> None:
        """Update position and velocity"""
        # Update velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.velocity.limit(self.max_speed)
        
        # Update position
        self.position = self.position + self.velocity
        
        # Reset acceleration
        self.acceleration = Vector2D(0, 0)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'lat': self.position.x,
            'lng': self.position.y,
            'outside_zone': self.outside_zone
        }

class CowHerd:
    """Manages a herd of cows with flocking behavior"""
    def __init__(self, field_center: Tuple[float, float], num_cows: int = 20):
        self.field_center = Vector2D(field_center[0], field_center[1])
        self.cows = []
        
        # Initialize cows in the field center (smaller initial spread)
        for i in range(num_cows):
            lat = field_center[0] + random.uniform(-0.003, 0.003)  # Smaller spread
            lng = field_center[1] + random.uniform(-0.003, 0.003)  # Smaller spread
            cow = Cow(f"cow_{i}", lat, lng)
            self.cows.append(cow)
    
    def update(self, drone_zone_center: Vector2D = None) -> None:
        """Update all cows with flocking behavior"""
        for cow in self.cows:
            # Get neighbors for this cow
            neighbors = [other for other in self.cows if other != cow]
            
            # Use drone zone center if available, otherwise use field center
            zone_center = drone_zone_center if drone_zone_center else self.field_center
            
            # Apply flocking behavior
            cow.flock(neighbors, zone_center)
            cow.update()
    
    def check_zone_exits(self, zone_polygon: List[Tuple[float, float]]) -> None:
        """Check which cows are outside the drone surveillance zone"""
        if not zone_polygon or len(zone_polygon) < 3:
            # If no valid zone, all cows are considered inside
            for cow in self.cows:
                cow.outside_zone = False
            print(f"No valid zone polygon, marking all {len(self.cows)} cows as inside")
            return
        
        inside_count = 0
        outside_count = 0
        
        for cow in self.cows:
            is_inside = self._point_in_polygon(
                cow.position.x, cow.position.y, zone_polygon
            )
            cow.outside_zone = not is_inside
            if is_inside:
                inside_count += 1
            else:
                outside_count += 1
        
        print(f"Zone check: {inside_count} inside, {outside_count} outside")
    
    def _point_in_polygon(self, x: float, y: float, polygon: List[Tuple[float, float]]) -> bool:
        """Ray casting algorithm to check if point is inside polygon"""
        inside = False
        n = len(polygon)
        if n == 0:
            return False
        
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def get_cows_data(self) -> List[Dict]:
        """Get all cows data for JSON serialization"""
        return [cow.to_dict() for cow in self.cows]
    
    def get_zone_center(self) -> Vector2D:
        """Calculate the center of the cow herd"""
        if not self.cows:
            return self.field_center
        
        sum_x = sum(cow.position.x for cow in self.cows)
        sum_y = sum(cow.position.y for cow in self.cows)
        
        return Vector2D(sum_x / len(self.cows), sum_y / len(self.cows))