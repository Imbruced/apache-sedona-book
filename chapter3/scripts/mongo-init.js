db = db.getSiblingDB("sedona");

db.createCollection("points");

db.points.createIndex({ location: "2dsphere" });

db.points.insertMany([
    {
        name: "Point A",
        location: {
            type: "Point",
            coordinates: [-74.0060, 40.7128]
        }
    },
    {
        name: "Point B",
        location: {
            type: "Point",
            coordinates: [-118.2437, 34.0522]
        }
    }
]);