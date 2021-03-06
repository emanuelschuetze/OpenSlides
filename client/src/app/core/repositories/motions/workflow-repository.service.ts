import { Injectable } from '@angular/core';

import { Workflow } from 'app/shared/models/motions/workflow';
import { ViewWorkflow } from 'app/site/motions/models/view-workflow';
import { DataSendService } from '../../core-services/data-send.service';
import { DataStoreService } from '../../core-services/data-store.service';
import { BaseRepository } from '../base-repository';
import { CollectionStringMapperService } from '../../core-services/collectionStringMapper.service';
import { WorkflowState } from 'app/shared/models/motions/workflow-state';
import { ViewMotion } from 'app/site/motions/models/view-motion';
import { HttpService } from 'app/core/core-services/http.service';
import { ViewModelStoreService } from 'app/core/core-services/view-model-store.service';
import { TranslateService } from '@ngx-translate/core';

/**
 * Repository Services for Categories
 *
 * The repository is meant to process domain objects (those found under
 * shared/models), so components can display them and interact with them.
 *
 * Rather than manipulating models directly, the repository is meant to
 * inform the {@link DataSendService} about changes which will send
 * them to the Server.
 */
@Injectable({
    providedIn: 'root'
})
export class WorkflowRepositoryService extends BaseRepository<ViewWorkflow, Workflow> {
    /**
     * The url to state on rest
     */
    private restStateUrl = 'rest/motions/state/';

    /**
     * Creates a WorkflowRepository
     * Converts existing and incoming workflow to ViewWorkflows
     *
     * @param DS Accessing the data store
     * @param mapperService mapping models
     * @param dataSend sending data to the server
     * @param httpService HttpService
     */
    public constructor(
        DS: DataStoreService,
        dataSend: DataSendService,
        mapperService: CollectionStringMapperService,
        viewModelStoreService: ViewModelStoreService,
        translate: TranslateService,
        private httpService: HttpService
    ) {
        super(DS, dataSend, mapperService, viewModelStoreService, translate, Workflow);

        this.sortedViewModelListSubject.subscribe(models => {
            if (models && models.length > 0) {
                this.initSorting(models);
            }
        });
    }

    public getVerboseName = (plural: boolean = false) => {
        return this.translate.instant(plural ? 'Workflows' : 'Workflow');
    };

    /**
     * Sort the states of custom workflows. Ignores simple and complex workflows.
     * Implying the default workflows always have the IDs 1 und 2
     *
     * TODO: Temp Solution. Should be replaced by general sorting over repositories after PR 4411
     *       This is an abstract to prevent further collisions. Real sorting is then done in 4411
     *       For now this "just" sorts the Workflow states of all custom workflows
     */
    private initSorting(workflows: ViewWorkflow[]): void {
        for (const workflow of workflows) {
            workflow.sortStates();
        }
    }

    /**
     * Creates a ViewWorkflow from a given Workflow
     *
     * @param workflow the Workflow to convert
     */
    protected createViewModel(workflow: Workflow): ViewWorkflow {
        const viewWorkflow = new ViewWorkflow(workflow);
        viewWorkflow.getVerboseName = this.getVerboseName;
        return viewWorkflow;
    }

    /**
     * Adds a new state to the given workflow
     *
     * @param stateName The name of the new Workflow
     * @param viewWorkflow The workflow
     */
    public async addState(stateName: string, viewWorkflow: ViewWorkflow): Promise<void> {
        const newStatePayload = {
            name: stateName,
            workflow_id: viewWorkflow.id
        };
        await this.httpService.post(this.restStateUrl, newStatePayload);
    }

    /**
     * Updates workflow state with a new value-object and sends it to the server
     *
     * @param newValue a key-value pair with the new state value
     * @param workflowState the workflow state to update
     */
    public async updateState(newValue: object, workflowState: WorkflowState): Promise<void> {
        const stateUpdate = Object.assign(workflowState, newValue);
        await this.httpService.put(`${this.restStateUrl}${workflowState.id}/`, stateUpdate);
    }

    /**
     * Deletes the selected work
     *
     * @param workflowState the workflow state to delete
     */
    public async deleteState(workflowState: WorkflowState): Promise<void> {
        await this.httpService.delete(`${this.restStateUrl}${workflowState.id}/`);
    }

    /**
     * Collects all existing states from all workflows
     *
     * @returns All currently existing workflow states
     */
    public getAllWorkflowStates(): WorkflowState[] {
        let states: WorkflowState[] = [];
        this.getViewModelList().forEach(workflow => {
            if (workflow) {
                states = states.concat(workflow.states);
            }
        });
        return states;
    }

    /**
     * Returns all workflowStates that cover the list of viewMotions given
     *
     * @param motions The motions to get the workflows from
     * @returns The workflow states to the given motion
     */
    public getWorkflowStatesForMotions(motions: ViewMotion[]): WorkflowState[] {
        let states: WorkflowState[] = [];
        const workflowIds = motions
            .map(motion => motion.workflow_id)
            .filter((value, index, self) => self.indexOf(value) === index);
        workflowIds.forEach(id => {
            const workflow = this.getViewModel(id);
            states = states.concat(workflow.states);
        });
        return states;
    }
}
