#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { NetworkStack } from '../lib/network-stack';
import { DatabaseStack } from '../lib/database-stack';
import { ComputeStack } from '../lib/compute-stack';
import { AIStack } from '../lib/ai-stack';

const app = new cdk.App();

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION || 'ap-south-1',
};

// Network Stack - VPC, Subnets, Security Groups
const networkStack = new NetworkStack(app, 'BharatAIHub-NetworkStack', {
  env,
  description: 'Network infrastructure for Bharat AI Hub',
});

// Database Stack - RDS, DynamoDB, ElastiCache
const databaseStack = new DatabaseStack(app, 'BharatAIHub-DatabaseStack', {
  env,
  vpc: networkStack.vpc,
  description: 'Database infrastructure for Bharat AI Hub',
});

// Compute Stack - Lambda, ECS, API Gateway
const computeStack = new ComputeStack(app, 'BharatAIHub-ComputeStack', {
  env,
  vpc: networkStack.vpc,
  database: databaseStack.database,
  cache: databaseStack.cache,
  description: 'Compute infrastructure for Bharat AI Hub',
});

// AI Stack - Bedrock, SageMaker endpoints
const aiStack = new AIStack(app, 'BharatAIHub-AIStack', {
  env,
  description: 'AI/ML infrastructure for Bharat AI Hub',
});

// Add dependencies
databaseStack.addDependency(networkStack);
computeStack.addDependency(databaseStack);
aiStack.addDependency(computeStack);

// Tags
cdk.Tags.of(app).add('Project', 'BharatAIHub');
cdk.Tags.of(app).add('Environment', process.env.ENVIRONMENT || 'development');
cdk.Tags.of(app).add('ManagedBy', 'CDK');

app.synth();
