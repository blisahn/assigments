namespace MovieApp.Models
{
    public class Movie
    {
        public int Id { get; set; }
        public required string Title { get; set; }
        public required string Director { get; set; }
        public required string[] Stars { get; set; }
        public required int ReleaseYear { get; set; }
        public required string ImageUrl { get; set; }
    }
}
