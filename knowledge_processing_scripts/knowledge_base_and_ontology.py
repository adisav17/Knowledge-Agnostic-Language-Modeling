import uuid

class Entity:
    def __init__(self, name, is_common_noun=False, attributes=None):
        self.id = str(uuid.uuid4())  # Unique identifier
        self.name = name
        self.is_common_noun = is_common_noun
        self.attributes = attributes if attributes else {}
        self.relationships = {}

    def add_relationship(self, relation_type, related_entity):
        self.relationships.setdefault(relation_type, set()).add(related_entity.id)

    def get_instances(self, ontology, relation_type='has_instance'):
        return [ontology.entities[entity_id].name for entity_id in self.relationships.get(relation_type, [])]

    def add_instances(self, instances, ontology, relation_type='has_instance', is_common_noun=False):
        if not isinstance(instances, list):
            instances = [instances]

        for instance_name in instances:
            instance_entity = ontology.find_entity_by_name(instance_name)
            if not instance_entity:
                instance_entity = Entity(name=instance_name, is_common_noun=is_common_noun)
                ontology.add_entity(instance_entity)
                print(f"Entity {instance_name} (ID: {instance_entity.id}) created and added to the ontology.")

            self.add_relationship(relation_type, instance_entity)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Relationship:
    def __init__(self, relation_type, entity1, entity2):
        self.relation_type = relation_type
        self.entity1 = entity1
        self.entity2 = entity2
        entity1.add_relationship(relation_type, entity2)
        entity2.add_relationship(self.inverse_relation(relation_type), entity1)

    def inverse_relation(self, relation_type):
        inverse_relations = {
        "subtype_of": "has_subtype",
        "instance_of": "has_instance"
        }
        return inverse_relations.get(relation_type, f"related_to_{relation_type}")
    


class Ontology:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity_name, is_common_noun=False, attributes=None):

        entity = Entity(entity_name, is_common_noun, attributes)
        self.entities[entity.id] = entity
        
            

    def find_entity_by_name(self, name):
        for entity in self.entities.values():
            if entity.name == name:
                return entity
        return None

    def add_relationship(self, relation_type, entity1, entity2):
        Relationship(relation_type, entity1, entity2)

    def get_hierarchy_list(self, entity, relation_type):
        hierarchy = []
        visited = set()

        def recurse(e):
            if e.id in visited:
                return
            visited.add(e.id)

            if relation_type in e.relationships:
                for related_entity_id in e.relationships[relation_type]:
                    related_entity = self.entities.get(related_entity_id)
                    if related_entity:
                        hierarchy.append(related_entity.name)
                        recurse(related_entity)

        recurse(entity)
        return hierarchy

    def get_hierarchy_tree(self, entity, relation_type):
        visited = set()

        def recurse(e):
            if e.id in visited:
                return None
            visited.add(e.id)

            hierarchy = [e.name]
            if relation_type in e.relationships:
                for related_entity_id in e.relationships[relation_type]:
                    related_entity = self.entities.get(related_entity_id)
                    if related_entity:
                        branch = recurse(related_entity)
                        if branch:
                            hierarchy.append(branch)

            return hierarchy

        return recurse(entity)
