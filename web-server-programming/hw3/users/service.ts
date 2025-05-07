import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { UsersComponent } from './component';

export interface User {
    name: string;
    email: string;
    city: string;
}

@Injectable({
    providedIn: 'root'
})
export class UserService {
    private http = inject(HttpClient);
    private apiUrl = 'https://jsonplaceholder.typicode.com/users'; // You'll provide this later

    constructor() { }

    getUsers(): Observable<User[]> {
        return this.http.get<any>(this.apiUrl).pipe(
            map(response => {
                // Map the API response to our User interface
                // Adjust property mapping based on your actual API response
                return response.map((item: { name: any; email: any; address: { city: any; }; city: any; }) => ({
                    name: item.name,
                    email: item.email,
                    city: item.address?.city || item.city // Handles different possible API formats
                }));
            })
        )
    }
}