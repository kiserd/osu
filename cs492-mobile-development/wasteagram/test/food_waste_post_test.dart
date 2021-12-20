import 'package:test/test.dart';
import 'package:wasteagram/models/food_waste_post_dto.dart';
import 'package:wasteagram/models/food_waste_post.dart';

void main() {
  test('food waste post constructed from map should have appropriate values',
      () {
    final date = DateTime.parse('2021-01-01');
    final url = 'someURL';
    final latitude = 10.0;
    final longitude = 10.0;
    final quantity = 100;

    final postMap = {
      'date': date,
      'imageURL': url,
      'latitude': latitude,
      'longitude': longitude,
      'quantity': quantity
    };

    final FoodWastePost post = FoodWastePost.fromDartMap(postMap);

    expect(post.date, date);
    expect(post.imageURL, url);
    expect(post.latitude, latitude);
    expect(post.longitude, longitude);
    expect(post.quantity, quantity);
  });

  test('empty food waste post DTO named constructor behaves as expected', () {
    final date = DateTime.parse('1900-01-01');
    final url = '';
    final latitude = 0;
    final longitude = 0;
    final quantity = 0;

    final FoodWastePostDTO post = FoodWastePostDTO.isEmpty();

    expect(post.date, date);
    expect(post.imageURL, url);
    expect(post.latitude, latitude);
    expect(post.longitude, longitude);
    expect(post.quantity, quantity);
  });

  test('assigning food waste post DTO values behaves as expected', () {
    final FoodWastePostDTO post = FoodWastePostDTO.isEmpty();
    post.date = DateTime.parse('1990-09-01');
    post.imageURL = 'fakeURL';

    final date = DateTime.parse('1990-09-01');
    final url = 'fakeURL';

    expect(post.date, date);
    expect(post.imageURL, url);
  });
}
