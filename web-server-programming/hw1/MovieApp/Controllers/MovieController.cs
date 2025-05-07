using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using MovieApp.Models;

namespace MovieApp.Controllers
{
    public class MovieController : Controller
    {
        private static List<Movie> movies = new List<Movie>()
        {
            new Movie
            {
                Id = 1,
                Director = "Brett Rander",
                ReleaseYear = 2006,
                Title = "Spider Man 2",
                Stars = new[] { "Patrick Stewart", "Hugh Jacman", "Haille Berry" },
                ImageUrl = "/images/spiderman-2.jpg",
            },
            new Movie
            {
                Id = 2,
                Director = "Sami Raimi",
                ReleaseYear = 2004,
                Title = "X-Men: The Last Stand",
                Stars = new[] { "Tobey Maigure", "Kristen Dunst", "Alfred Molina" },
                ImageUrl = "/images/xmen.jpg",
            },
            new Movie
            {
                Id = 3,
                Director = "Sami Raimi",
                ReleaseYear = 2004,
                Title = "Spider Man 3",
                Stars = new[] { "Tobey Maigure", "Kristen Dunst", "Topher Grace" },
                ImageUrl = "/images/spiderman-3.jpg",
            },
            new Movie
            {
                Id = 4,
                Title = "Valkyrie",
                Director = "Bryan Singer",
                Stars = new[] { "Tom Cruise", "Bill Nighy", "Carice van Houten" },
                ReleaseYear = 2008,
                ImageUrl = "/images/walkyrie.jpeg",
            },
            new Movie
            {
                Id = 5,
                Title = "Gladiator",
                Director = "Ridley Scott",
                Stars = new[] { "Russell Crowe", "Joaquin Phoenix", "Connie Nielsen" },
                ReleaseYear = 2000,
                ImageUrl = "/images/gladiator.jpeg",
            },
        };

        private static HashSet<Movie> cart = new HashSet<Movie>();

        public IActionResult Index()
        {
            return View(movies);
        }

        public IActionResult Details(int? id)
        {
            if (id == null)
            {
                TempData["ErrorMessage"] = "Please specify a Movie Id!";
                return View("MovieInfo");
            }

            var movie = movies.FirstOrDefault(m => m.Id == id);
            if (movie == null)
            {
                TempData["ErrorMessage"] = "Invalid Movie Id!";
                return View("MovieInfo");
            }

            return View("MovieInfo", movie);
        }

        public IActionResult AddToCart(int movieId)
        {
            var firstName = Request.Cookies["FirstName"];
            var lastName = Request.Cookies["LastName"];

            if (string.IsNullOrEmpty(firstName) || string.IsNullOrEmpty(lastName))
            {
                TempData["ErrorMessage"] = "You need to log in to add a movie to your cart.";
                return RedirectToAction("Details", "Movie", new { id = movieId });
            }

            var movie = movies.FirstOrDefault(m => m.Id == movieId);
            if (movie != null)
            {
                if (cart.Add(movie) == false)
                {
                    TempData["ErrorMessage"] = "Movie is already in your cart!";
                }
                else
                {
                    TempData["SuccessMessage"] = "Movie successfully added to your cart!";
                }
            }

            return RedirectToAction("Details", "Movie", new { id = movieId });
        }

        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Login(string firstName, string lastName)
        {
            if (string.IsNullOrWhiteSpace(firstName) || string.IsNullOrWhiteSpace(lastName))
            {
                ViewBag.ErrorMessage = "Both first name and last name are required!";
                return View();
            }

            Response.Cookies.Append(
                "FirstName",
                firstName,
                new CookieOptions { Expires = DateTime.Now.AddMonths(1) }
            );
            Response.Cookies.Append(
                "LastName",
                lastName,
                new CookieOptions { Expires = DateTime.Now.AddMonths(1) }
            );

            return RedirectToAction("Index");
        }

        public IActionResult Cart()
        {
            return View(cart);
        }

        public IActionResult Logout()
        {
            Response.Cookies.Delete("FirstName");
            Response.Cookies.Delete("LastName");
            cart.Clear();
            TempData["SuccessMessage"] = "You have been successfully logged out.";
            return RedirectToAction("Index");
        }
    }
}
