module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      object: String,
      description: String,
      row: String,
      columm: String,
      condition: String,
      state: String,
      id: String
    },
    { timestamps: true }
  );

  schema.method("toJSON", function() {
    const { __v, _id, ...object } = this.toObject();
    object.id = _id;
    return object;
  });

  const Tutorial = mongoose.model("shelf", schema);
  return Tutorial;
};
