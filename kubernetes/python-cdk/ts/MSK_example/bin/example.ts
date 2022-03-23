#!/usr/bin/env node
import 'source-map-support/register';
import cdk = require('@aws-cdk/core');

import { VPCStack } from "../lib/Vpc";
import { MskClusterStack } from "../lib/MskCluster";

const app = new cdk.App();
const app_env = {
    region: <account region>,
    account: <account number>
};

const vpcStack = new VPCStack(app, 'VPCStack', {env: app_env});
new MskClusterStack(app, 'MskClusterStack',{env: app_env, vpc: vpcStack.Vpc});
