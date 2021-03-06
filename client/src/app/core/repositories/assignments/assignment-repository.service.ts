import { Injectable } from '@angular/core';

import { TranslateService } from '@ngx-translate/core';

import { Assignment } from 'app/shared/models/assignments/assignment';
import { BaseAgendaContentObjectRepository } from '../base-agenda-content-object-repository';
import { CollectionStringMapperService } from '../../core-services/collectionStringMapper.service';
import { DataSendService } from 'app/core/core-services/data-send.service';
import { DataStoreService } from '../../core-services/data-store.service';
import { Item } from 'app/shared/models/agenda/item';
import { Tag } from 'app/shared/models/core/tag';
import { User } from 'app/shared/models/users/user';
import { ViewAssignment } from 'app/site/assignments/models/view-assignment';
import { ViewItem } from 'app/site/agenda/models/view-item';
import { ViewModelStoreService } from 'app/core/core-services/view-model-store.service';
import { ViewTag } from 'app/site/tags/models/view-tag';
import { ViewUser } from 'app/site/users/models/view-user';

/**
 * Repository Service for Assignments.
 *
 * Documentation partially provided in {@link BaseRepository}
 */
@Injectable({
    providedIn: 'root'
})
export class AssignmentRepositoryService extends BaseAgendaContentObjectRepository<ViewAssignment, Assignment> {
    /**
     * Constructor for the Assignment Repository.
     *
     * @param DS The DataStore
     * @param mapperService Maps collection strings to classes
     */
    public constructor(
        DS: DataStoreService,
        dataSend: DataSendService,
        mapperService: CollectionStringMapperService,
        viewModelStoreService: ViewModelStoreService,
        translate: TranslateService
    ) {
        super(DS, dataSend, mapperService, viewModelStoreService, translate, Assignment, [User, Item, Tag]);
    }

    public getAgendaTitle = (assignment: Partial<Assignment> | Partial<ViewAssignment>) => {
        return assignment.title;
    };

    public getAgendaTitleWithType = (assignment: Partial<Assignment> | Partial<ViewAssignment>) => {
        return assignment.title + ' (' + this.getVerboseName() + ')';
    };

    public getVerboseName = (plural: boolean = false) => {
        return this.translate.instant(plural ? 'Elections' : 'Election');
    };

    public createViewModel(assignment: Assignment): ViewAssignment {
        const relatedUser = this.viewModelStoreService.getMany(ViewUser, assignment.candidates_id);
        const agendaItem = this.viewModelStoreService.get(ViewItem, assignment.agenda_item_id);
        const tags = this.viewModelStoreService.getMany(ViewTag, assignment.tags_id);

        const viewAssignment = new ViewAssignment(assignment, relatedUser, agendaItem, tags);
        viewAssignment.getVerboseName = this.getVerboseName;
        viewAssignment.getAgendaTitle = () => this.getAgendaTitle(viewAssignment);
        viewAssignment.getAgendaTitleWithType = () => this.getAgendaTitleWithType(viewAssignment);
        return viewAssignment;
    }
}
