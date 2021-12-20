class FoodWastePostDTO {
  // fields
  late DateTime date;
  late String imageURL;
  late int quantity;
  late double? latitude;
  late double? longitude;

  // constructors
  FoodWastePostDTO.isEmpty() {
    this.date = DateTime.parse('1900-01-01');
    this.imageURL = '';
    this.quantity = 0;
    this.latitude = 0;
    this.longitude = 0;
  }
}
