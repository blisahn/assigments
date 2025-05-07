import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { UsersComponent } from './component';

@NgModule({
    declarations: [
        UsersComponent
    ],
    imports: [
        CommonModule,
    ],
    exports: [
        UsersComponent
    ]
})
export class UsersModule { }