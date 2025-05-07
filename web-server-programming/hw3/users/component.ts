import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { UserService } from './service';


interface User {
    name: string,
    email: string,
    city: string
}

@Component({
    selector: 'app-users',
    standalone: true,
    imports: [CommonModule],
    templateUrl: 'component.html',
    styleUrls: ['component.css']
})

export class UsersComponent implements OnInit {

    users: User[] = []
    constructor(private userService: UserService) {

    }
    ngOnInit(): void {
        this.userService.getUsers().subscribe({
            next: (data) => {
                this.users = data;
            },
            error: (err) => {
                console.error('Error fetching users:', err);
            }
        });
    }
}