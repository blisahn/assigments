import { Routes } from '@angular/router';
import { UsersComponent } from '../app/users/component';

export const routes: Routes = [
    { path: '', redirectTo: '/users', pathMatch: 'full' },
    { path: 'users', component: UsersComponent },
];
